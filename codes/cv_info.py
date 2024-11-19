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
    """ "
    This function extracts the professional summary from a CV. If the professional summary is not found,
    the function will prompt the user to provide the professional summary.
    """
    prof_summary = re.search(
        r"(PROFESSIONAL SUMMARY|SUMMARY)(.*?)(PROFESSIONAL|EXPERIENCE)", cv, re.DOTALL
    )
    if prof_summary:
        return prof_summary.group(2).replace("**", "").strip()
    else:
        system_msg = "You are a helpful assistant helping me to extract professional summary from a CV.\
            You shall only answer me with the summary, nothing else. The CV content is as follows:"
        return chatgpt("gpt-4o-mini", cv, system_msg=system_msg)
