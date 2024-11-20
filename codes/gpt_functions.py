import os
import re
import ast
import fuzzywuzzy
import tkinter as tk
import pandas as pd

from config import *
from cv_info import *
from openai import OpenAI
from PyPDF2 import PdfMerger
from tkinter import messagebox


def chatgpt(model, prompt, system_msg=None, last_prompt=None, last_answer=None, temp=0):
    client = OpenAI(api_key=api_key)
    model = model
    prompt = prompt

    messages = []

    if system_msg:
        messages.append({"role": "system", "content": system_msg})

    if last_prompt and last_answer:
        messages.append({"role": "user", "content": last_prompt})
        messages.append({"role": "assistant", "content": last_answer})

    messages.append({"role": "user", "content": prompt})

    # Create chat completion request
    chat_completion = client.chat.completions.create(
        messages=messages, model=model, temperature=temp
    )

    # Get the assistant's answer
    answer = chat_completion.choices[0].message.content
    return answer


def query_companyinfo(jd_required):
    prompt = f"""
    I am providing you with a job description. Use the information in the job description, help me **extract** company's name and address line (two lines), city and state. Use state abbreviation if possible.\n\nBe concise, and only provide the requested information. If any information I am providing you is missing, response "None" in that sector.\n\n**Job Description**\n{jd_required}\n\n**Company Name:**\n\n\n**Company Address Line 1:**\n\n\n**Company Address Line 2:**\n\n\n**City:**\n\n\n**State:**\n
    """
    return prompt


def company_info(
    info,
    company_name,
    company_address_line_1,
    company_address_line_2,
    company_city,
    company_state_two_letter,
    company_country,
):
    info = info.replace(r"\n\n", r"\n")

    pattern = r"\*\*Company Name:\*\*\s*(.*?)\s*\n\*\*Company Address Line 1:\*\*\s*(.*?)\s*\n\*\*Company Address Line 2:\*\*\s*(.*?)\s*\n\*\*City:\*\*\s*(.*?)\s*\n\*\*State:\*\*\s*([A-Za-z]{2,})\s*"

    results = re.match(pattern, info, re.DOTALL)
    company_name = (
        results.group(1).replace("*", "").strip()
        if company_name == ""
        else company_name
    )

    company_address_line_1 = (
        results.group(2).replace("*", "").strip()
        if company_address_line_1 == ""
        else company_address_line_1
    )

    company_address_line_2 = (
        results.group(3).replace("*", "").strip()
        if company_address_line_2 == ""
        else company_address_line_2
    )

    company_city = (
        results.group(4).replace("*", "").strip()
        if company_city == ""
        else company_city
    )

    company_state_two_letter = (
        results.group(5).replace("*", "").strip()
        if company_state_two_letter == ""
        else company_state_two_letter
    )

    if company_state_two_letter in us_state_dict.keys():
        company_country = "USA"
    elif company_state_two_letter in ca_province_dict.keys():
        company_country = "Canada"
    elif company_state_two_letter in ["None", ""]:
        company_country = "None"
    else:
        assert (
            False
        ), f"State / Province {company_state_two_letter} not found in state_dict"

    return (
        True,
        company_name,
        company_address_line_1,
        company_address_line_2,
        company_city,
        company_state_two_letter,
        company_country,
    )


null_answers = ["", "None", "N/A"]


def judge_info_type(
    company_name, company_address_line_1, company_address_line_2, company_city
):
    if company_address_line_1 in null_answers and company_name in null_answers:
        assert False, "Company name and address line 1 cannot be empty"
    elif company_city in null_answers:
        assert False, "City cannot be empty"
    elif (
        company_address_line_1 not in null_answers
        and company_address_line_2 in null_answers
    ):
        status = "single_line"
    elif company_address_line_1 in null_answers:
        status = "no_address"
    else:
        status = "full_address"

    return True, status


def query_something_important(jd_required):
    query = f"""
    I am applying for a job. I will attach the job description below. I did not take a look at the job description, and I plan to submit my CV and tailored cover letter to the system. Please warn me if there is anything I need to have my files modified or is there any extra files needed to prepare. For example, I need to combine them; I need to arrange them in a specific order; Some more documents needed, etc.\n\nPlease be very concise, tell me only conclusion. If what I prepared is just enough, please respond "Nothing needed".\n\n**Job Description:**\n{jd_required}\n\n**Things to note:**
    """

    return query


def query_anything_turn_me_down(jd_required):
    query = f"""
    I am applying for a job. I will attach the job description below. I did not take a look at the job description, and I plan to submit my CV and tailored cover letter to the system. Please warn me if there is anything that may turn me down. For example, I am not qualified for this job; I am not eligible to work in this country; I am not available to work at this time, there is a specific requirement that I do not meet, etc.\n\nPlease be very concise, tell me only conclusion. If nothing will turn me down, please respond "Nothing needed".\n\n**Job Description:**\n{jd_required}\n\n**Things to note:**
    """
    return query


def beep(system_used):
    if system_used == "Windows":
        import winsound

        winsound.MessageBeep(winsound.MB_ICONHAND)
    else:
        os.system("afplay /System/Library/Sounds/Blow.aiff")


def show_popup(answer, system_used, turnmedown):
    if system_used == "Windows":
        root = tk.Tk()
        root.withdraw()
        if not turnmedown:
            messagebox.showinfo("Notice when applying for this job", answer)
        else:
            messagebox.showinfo("Something will turn you down", answer)

        root.destroy()

    else:
        if not turnmedown:
            os.system(
                f'osascript -e \'tell app "System Events" to display dialog "{answer}" with title "Notice when applying for this job"\''
            )
        else:
            os.system(
                f'osascript -e \'tell app "System Events" to display dialog "{answer}" with title "Something will turn you down"\''
            )


def judge_something_important(answer, package_folder, system_used, turnmedown=False):
    showed_popup = False
    if re.search("nothing needed", answer, re.IGNORECASE) is None:
        show_popup(answer, system_used, turnmedown)
        showed_popup = True
        if not turnmedown:
            with open(f"{package_folder}/things_to_note.txt", "w") as f:
                f.write(answer)
        else:
            with open(f"{package_folder}/things_to_note_turn_me_down.txt", "w") as f:
                f.write(answer)
    return showed_popup


def query_cover_letter(
    cv_to_use, jd_required, company_name, additional_strength_to_mention=None
):
    prompt = f"""{one_sentence_bio}. Now I am seeking jobs in financial industries. Now I will provide you with a job description and my resume, and I want you to help me write a cover letter based on the job description and my resume. Please keep the cover letter concise and professional.\n\nNotice, you shouldn't make it feel too much like AI. Specifically, don't use too many adverbial phrases.\n\nMoreover, the cover letter should make my strengths clear at a glance, and my cover letter should be divided into these parts: who I am, what aspects I want to emphasize for this job, and why I like this job.\n\nPlease also make important texts bold by using **, . Do not only bold the first paragraph. In my working experience there should also be something worth bolding.\n\nDo not bold too many texts, only bold most important ones.\n\nPlease try to keep the cover letter less than 300 words, but it is not a must. The most important thing is to make it concise and professional.
    
    **Company Name:**
    {company_name}
    
    **Job Description:**
    {jd_required}
    
    **My Resume:**
    {cv_to_use}
    
    **Please mention some of my strongest points in the cover letter:**
    {additional_strength_to_mention if additional_strength_to_mention else ""}
    
    **Cover Letter:**
    """
    return prompt


def query_shirnk_text(extracted_text, threshold=300):
    query = f"""
    Please help me shrink the cover letter to less than {threshold} words while keeping the main content and etiquette.\n\nRemember to again bold the important texts that are marked with ** in the original cover letter.\n\n**Cover Letter:**\n{extracted_text}\n\n**Shrinked Cover Letter:**
    """
    return query


def shrink_text(extracted_text, threshold=300):
    word_count_original = len(extracted_text.split())
    if word_count_original < threshold:
        print(
            f"No need to shrink the text. The original text is already less than {threshold} words: {word_count_original} words."
        )
        return extracted_text

    extracted_text_2 = chatgpt("chatgpt-4o-latest", query_shirnk_text(extracted_text))
    word_count_2 = len(extracted_text_2.split())

    print(
        f"Shrinked. New word count {word_count_2}, original word count {word_count_original}"
    )
    return extracted_text_2


def query_job_title(jd_required, cv_to_use, cover_letter):
    prompt = f"""
    I will provide you with a job description,  my resume, and my drafted cover letter.\n\nI want you to help me identify the job title I shall use in my cover letter: for example "Research Intern", "Assistant Portfolio Manager", "Execution Trader", etc. You can use "&" to connect two titles if necessary. Remember, this job title is used to describe **my position**.\n\nDo not use any title that is not related to my position or too boastful.\n\nAlso. just give me the result. Do not give me the reasoning.\n\n**Job Description:**\n{jd_required}\n\n**My Resume:**\n{cv_to_use}\n\n**Drafted Cover Letter:**
    {cover_letter}\n\n**Most Suitable Job Title:**
    """
    return prompt


def merge_pdf(sequence, package_folder, my_name):
    # Locate pdfs
    try:
        open(f"{package_folder}/CV - {my_name}.pdf")
    except FileNotFoundError:
        assert False, f"{package_folder}/CV - {my_name}.pdf not found"
    try:
        open(f"{package_folder}/Cover Letter - {my_name}.pdf")
    except FileNotFoundError:
        assert False, f"{package_folder}/Cover Letter - {my_name}.pdf not found"
    try:
        open(f"{package_folder}/Unofficial Transcript - {my_name}.pdf")
    except FileNotFoundError:
        assert (
            False
        ), f"{package_folder}/Unofficial Transcript - {my_name}.pdf not found"

    pdf_dict = {
        "1": f"{package_folder}/CV - {my_name}.pdf",
        "2": f"{package_folder}/Cover Letter - {my_name}.pdf",
        "3": f"{package_folder}/Unofficial Transcript - {my_name}.pdf",
    }

    merger = PdfMerger()
    pdfs = [pdf_dict[x] for x in sequence]
    for pdf in pdfs:
        merger.append(pdf)

    merger.write(f"{package_folder}/{my_name} - Application.pdf")
    merger.close()

    return True


def extract_keywords(jd, cv, company_name, company_country):
    system_msg_1 = f"""You are an ATS (Applicant Tracking System) machine screener, filtering resumes received for the job opening at {company_name} in {company_country}. Here is the job description for this role:\n\n{jd}\n\nNow you received one applicant (me)'s CV: \n\n{cv}\n\nEvaluate thoroughly the key abilities required for this role, and evaluate my CV's ATS compatibility by analyzing keyword matches and formatting. Score on a scale of 0-100, where 100 means perfect keyword alignment and formatting, and 0 means no matches. If the score surpasses 70, my CV can go through this round of machine screening, meaning it is a compatible CV. Use industry-recognized ATS standards to evaluate my CV."""

    prompt_1 = """On a scale of 0-100, please provide my CV's ATS score. Output only the number, do not include any other information."""

    # First attempt with no temperature
    answer_1 = chatgpt("gpt-4o-mini", prompt=prompt_1, system_msg=system_msg_1)
    try:
        ats_score_num = int(answer_1)
        if 0 <= ats_score_num <= 100:
            if ats_score_num >= 70:
                return True, ats_score_num, []
    except ValueError:
        pass

    # Retry with increasing temperature if initial attempt fails
    for retry in range(1, 5):
        try:
            answer_1 = chatgpt(
                "gpt-4o-mini",
                prompt=prompt_1,
                system_msg=system_msg_1,
                temp=0.2 * retry,
            )
            ats_score_num = int(answer_1)
            if 0 <= ats_score_num <= 100:
                break
        except ValueError:
            continue
    else:
        return False, 0, []

    system_msg_2 = f"""You are a professional HR manager working for {company_name} in {company_country}. You are supposed to help me refine my resume to better match a role in this company. The job description for this role: \n\n{jd}\n\nMy CV has already went through the ATS screening and the machine provided me with a score {ats_score_num}."""

    if ats_score_num >= 70:
        prompt_2 = f"""This ATS score means my CV has already passed the machine screening. However, as a professional HR, please help me identify what keywords or key abilities required by this role failed to show up in my CV."""

    else:
        prompt_2 = f"""This means my CV lacks some important keywords or abilities that disqualifies me from this round of machine screening.\n\nNow, I want you, the professional HR, to help me identify what keywords or key abilities required by this role failed to show up in my CV."""

    prompt_2 += """\n\nNote that you have to extract the ability I failed to mention in my resume instead of copying and pasting phrases from job description. For example, if the job description mentions 'customer focused culture' and 'client relationships' that fails to show up in my CV, you should only extract keyword "client-facing" from these phrases instead of pasting the whole phrases.\n\nFormat your output in Python list format, like: ['keyword1', 'keyword2', 'keyword3']. Do not include any other information in the output."""

    for retry in range(5):
        answer_2 = (
            chatgpt("gpt-4o-mini", prompt=prompt_2, system_msg=system_msg_2)
            .strip()
            .replace("```python", "")
            .replace("`", "")
        )

        try:
            return True, ats_score_num, ast.literal_eval(answer_2)
        except Exception:
            continue

    return False, ats_score_num, []


def show_popup_keyword(system_used, kw_list, ats_score):
    if system_used == "Windows":
        root = tk.Tk()
        root.withdraw()
        choice = messagebox.askyesno(
            "Keywords missing in CV",
            f"""ATS Score: {ats_score}. Keywords missing in CV: {', '.join(kw_list)}, please change "base.docx" accordingly. After changing "base.docx", please click "Already Changed". If you decline the suggestions, please click "Decline Suggestion".""",
            icon="question",
            button={"yes": "Already Changed", "no": "Decline Suggestion"},
        )
        root.destroy()

        if choice:
            return "Already changed"
        else:
            return "Decline suggestion"

    else:
        script = f"""
            tell application "System Events"
            set theButton to button returned of (display dialog "ATS Score: {ats_score}. Keywords missing in CV: {', '.join(kw_list)}, please change \\"base.docx\\" accordingly. After changing \\"base.docx\\", please click \\"Already Changed\\". If you decline the suggestions, please click \\"Decline Suggestion\\"." buttons {{"Already Changed", "Decline Suggestion"}} default button "Already Changed")
            end tell
        """
        result = os.system(f"osascript -e '{script}'")

        if result == 0:
            return "Already changed"
        else:
            return "Decline suggestion"


def compare_jd(jd, company_name, df, threshold=90):
    jd_text = jd.replace("\n", " ")
    applied_key = range(len(df))
    applied_val = df["Original_JD"].apply(lambda x: x.replace("\n", " ")).tolist()
    applied = dict(zip(applied_key, applied_val))
    scores_val = [fuzzywuzzy.fuzz.token_set_ratio(jd_text, x) for x in applied.values()]
    scores = dict(zip(applied_key, scores_val))

    scores_over_th = {k: v for k, v in scores.items() if v >= threshold}

    if len(scores_over_th) > 0:
        scores_over_th_idx = list(scores_over_th.keys())
        temp = df.loc[scores_over_th_idx][
            ["Date", "Company_Name", "Position_Name", "Company_City"]
        ]
        company_names_applied = temp["Company Name"].tolist()
        company_names_scores = [
            fuzzywuzzy.fuzz.token_set_ratio(company_name, x)
            for x in company_names_applied
        ]
        if any([x >= threshold for x in company_names_scores]):
            return True, "Similar applications found with similar company names.", temp

        else:
            return (
                True,
                "Similar applications found without similar company names.",
                temp,
            )

    else:
        return (
            False,
            "No similar applications found, feel free to proceed.",
            pd.DataFrame(),
        )


def msgbox_similar_application(message, temp, system_used):
    if system_used == "Windows":
        root = tk.Tk()
        root.withdraw()
        choice = messagebox.askyesno(
            "Similar Applications Found",
            f"{message}\n\n{temp.to_string()}",
            icon="warning",
            button={"yes": "Continue", "no": "Stop"},
        )
        root.destroy()
        if not choice:
            return "halt"

    else:
        script = f"""
            tell application "System Events"
            set theButton to button returned of (display dialog "{message}\n\n{temp.to_string()}" buttons {{"Continue", "Stop"}} default button "Continue")
            end tell
        """
        result = os.system(f"osascript -e '{script}'")

        if result != 0:
            return "halt"

    return "continue"
