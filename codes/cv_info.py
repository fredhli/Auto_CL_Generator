import re
from config import *
from gpt_functions import *


def get_cv(cv_type):
    """
    This function returns the content of a CV based on the CV type.
    """
    return cv_dict[cv_type]


def cv_location(cv_folder, cv_type):
    """
    This function returns the location of a CV based on the CV type.
    """
    return f"{cv_folder}/{cv_location_dict[cv_type]}"


def get_professional_summary(cv):
    """"
    This function extracts the professional summary from a CV. If the professional summary is not found, 
    the function will prompt the user to provide the professional summary.
    """
    prof_summary = re.search(
        r"(PROFESSIONAL SUMMARY|SUMMARY)(.*?)(PROFESSIONAL|EXPERIENCE)", cv, re.DOTALL)
    if prof_summary:
        return prof_summary.group(2).replace("**", "").strip()
    else:
        system_msg = "You are a helpful assistant helping me to extract professional summary from a CV.\
            You shall only answer me with the summary, nothing else. The CV content is as follows:"
        return chatgpt("gpt-4o-mini", cv, system_msg=system_msg)


def help_me_choose_cv(
    jd_required,
    cv_i_chose,
    cv_trader_quant_data=cv_trader_quant_data,
    cv_research=cv_research,
    cv_equity_research=cv_equity_research,
    cv_pan_finance=cv_pan_finance,
    cv_ibd=cv_ibd,
    cv_operation=cv_operation,
    cv_risk=cv_risk,
):

    jd_clean = jd_required.replace("\n", " ")

    system_msg = f"""
    You are a helpful assistant helping a job seeker choose the best CV version to apply for a job.\
    The job description goes as follows: {jd_clean}
    """

    query = f"""
    **Return me with **version name** of the most suitable CV to use based on each version of my CV's \
    professional summary section, no need to tell me CV content or state any reasons.
    **Version name: "trader_quant_data":**
    {get_professional_summary(cv_trader_quant_data)}

    **Version name: "research":**
    {get_professional_summary(cv_research)}

    **Version name: "equity_research":**
    {get_professional_summary(cv_equity_research)}

    **Version name: "pan_finance":**
    {get_professional_summary(cv_pan_finance)}

    **Version name:"ibd":**
    {get_professional_summary(cv_ibd)}

    **Version name: "operation":**
    {get_professional_summary(cv_operation)}

    **Version name: "risk":**
    {get_professional_summary(cv_risk)}
    """

    model = "gpt-4o-mini"
    retry_max = 5
    retry = 0
    valid_versions = cv_dict.keys()

    while retry < retry_max:
        try:
            answer = chatgpt(model, query, system_msg=system_msg)
            if answer:
                answer_clean = (
                    answer.lower().replace("version", "").replace("name", "").strip()
                )
                answer_clean = re.sub(r"[^\w\s]", "", answer_clean).strip()

                if answer_clean in valid_versions:
                    if not cv_i_chose == "undecided":
                        new_prompt = f"""
                        You chose version "{answer_clean} while my previous choice was "{cv_i_chose}.\
                        I am not saying that my choice is more superior and well-rounded, but can \
                        you please tell me your reasoning for choosing {answer_clean} within two \
                        sentences? If you changed your mind, please also let me know. Thank you!
                        """
                    else:
                        new_prompt = f"""You chose version "{answer_clean}. Please tell me your \
                        reasoning for choosing this version within two sentences. Thank you!"""

                    reason = chatgpt(
                        model=model,
                        prompt=new_prompt,
                        system_msg=system_msg,
                        last_prompt=query,
                        last_answer=answer,
                    )
                    return answer_clean, reason
            retry += 1
        except Exception as e:
            print(f"Error during chatgpt call: {e}")
            retry += 1

    # If no valid answer is found after retries
    print("Unable to determine the most suitable CV version.")
    return answer_clean, None
