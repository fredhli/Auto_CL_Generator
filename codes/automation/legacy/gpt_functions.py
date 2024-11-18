import os
import re
import tkinter as tk

from cv_info import *
from openai import OpenAI
from PyPDF2 import PdfMerger
from tkinter import messagebox


api_key = "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"

us_state_dict = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}

ca_province_dict = {
    "AB": "Alberta",
    "BC": "British Columbia",
    "MB": "Manitoba",
    "NB": "New Brunswick",
    "NL": "Newfoundland and Labrador",
    "NS": "Nova Scotia",
    "NT": "Northwest Territories",
    "NU": "Nunavut",
    "ON": "Ontario",
    "PE": "Prince Edward Island",
    "QC": "Quebec",
    "SK": "Saskatchewan",
    "YT": "Yukon",
}


def get_folders(root):
    return root, f"{root}/Cover Letter", f"{root}/CV", f"{root}/Package"


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
    I am providing you with a job description. Use the information in the job description, help me **extract** company's name and address line (two lines), city and state. Use state abbreviation if possible.

    Be concise, and only provide the requested information. If any information I am providing you is missing, response "None" in that sector.

    **Job Description**
    {jd_required}

    **Company Name:**

    **Company Address Line 1:**

    **Company Address Line 2:**

    **City:**

    **State:**
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
    I am applying for a job. I will attach the job description below. I did not take a look at the job description,\
    and I plan to submit my CV and tailored cover letter to the system.\
    Please warn me if there is anything I need to have my files modified or is there any extra files needed to prepare.\
    For example, I need to combine them; I need to arrange them in a specific order; Some more documents needed, etc.
    
    Please be very concise, tell me only conclusion. If what I prepared is just enough, please respond "Nothing needed".
    
    **Job Description:**
    {jd_required}
    
    **Things to note:**
    """

    return query


def query_anything_turn_me_down(jd_required):
    query = f"""
    I am applying for a job. I will attach the job description below. I did not take a look at the job description,\
    and I plan to submit my CV and tailored cover letter to the system.\
    Please warn me if there is anything that may turn me down. For example, I am not qualified for this job; I am not eligible to work in this country; I am not available to work at this time,\
    there is a specific requirement that I do not meet, etc.
    
    Please be very concise, tell me only conclusion. If nothing will turn me down, please respond "Nothing needed".
    
    **Job Description:**
    {jd_required}
    
    **Things to note:**
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
    prompt = f"""
    I am a top student in Quantitative Finance at Washington University in St. Louis with a GPA of 3.95/4.00. Now I am seeking jobs in financial industries. Now I will provide you with a job description\
    and my resume, and I want you to help me write a cover letter based on the job description and my resume. Please keep the cover letter concise and professional, 
    
    Notice, you shouldn't make it feel too much like AI. Specifically, don't use too many adverbial phrases.
    
    Moreover, the cover letter should make my strengths clear at a glance, and my cover letter should be divided into these parts: who I am, what aspects I want \
    to emphasize for this job, and why I like this job.
    
    Please also make important texts bold by using **, . Do not only bold the first paragraph. In my working experience there should also be something worth bolding.
    
    Do not bold too many texts, only bold most important ones.
    
    Please try to keep the cover letter less than 300 words, but it is not a must. The most important thing is to make it concise and professional.
    
    **Company Name:**
    {company_name}
    
    **Job Description:**
    {jd_required}
    
    **My Resume:**
    {cv_to_use}
    
    **Please mention some of my strongest points in the cover letter:**
    - I am a top student in Quantitative Finance at Washington University in St. Louis with an impressive GPA of 3.95/4.00.
    - I am eligible to work in Canada without sponsorship.
    {additional_strength_to_mention if additional_strength_to_mention else ""}
    
    **Cover Letter:**
    """
    return prompt


def query_shirnk_text(extracted_text, threshold=300):
    query = f"""
    Please help me shrink the cover letter to less than {threshold} words while keeping the main content and etiquette.
    
    Remember to again bold the important texts that are marked with ** in the original cover letter.
    
    **Cover Letter:**
    {extracted_text}
    
    **Shrinked Cover Letter:**
    """
    return query


def shrink_text(extracted_text, threshold=300):
    word_count_original = len(extracted_text.split())
    if word_count_original < threshold:
        print(
            f"No need to shrink the text. The original text is already less than {threshold} words: {word_count_original} words."
        )
        return extracted_text

    extracted_text_2 = chatgpt(
        "chatgpt-4o-latest", query_shirnk_text(extracted_text))
    word_count_2 = len(extracted_text_2.split())

    print(
        f"Shrinked. New word count {word_count_2}, original word count {word_count_original}"
    )
    return extracted_text_2


def query_job_title(jd_required, cv_to_use, cover_letter):
    prompt = f"""
    I will provide you with a job description,  my resume, and my drafted cover letter.\
    I want you to help me identify the job title I shall use in my cover letter: for example \
    "Data Scientist", "Assistant Portfolio Manager", "Execution Trader", etc. You can use "&" \
    to connect two titles if necessary. Remember, this job title is used to describe **my position**.
    
    Do not use any title that is not related to my position or too boastful .
    
    Also. just give me the result. Do not give me the reasoning.
    
    **Job Description:**
    {jd_required}
    
    **My Resume:**
    {cv_to_use}
    
    **Drafted Cover Letter:**
    {cover_letter}
    
    **Most Suitable Job Title:**
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


def chatgpt_with_system_message(model, prompt, system_msg, temp=0):
    client = OpenAI(api_key=api_key)

    messages = [{"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}]

    # Create chat completion request
    chat_completion = client.chat.completions.create(
        messages=messages, model=model, temperature=temp
    )

    # Get the assistant's answer
    answer = chat_completion.choices[0].message.content
    return answer
