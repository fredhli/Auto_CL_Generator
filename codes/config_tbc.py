import os
import re

# Your name here
my_name = ""

# One sentence bio means how you would introduce yourself before submitting a query to ChatGPT
one_sentence_bio = ""

# Notion page ID here, it's best to store this in an environment variable
page_id = os.getenv("NOTION_PAGE_ID")

# ChatGPT API key here, it's best to store this in an environment variable
api_key = os.getenv("CHATGPT_API_KEY")

# Notion API key here, it's best to store this in an environment variable
notion_key = os.getenv("NOTION_API_KEY")

# Google Maps API key here, it's best to store this in an environment variable
maps_key = os.getenv("GMAP_API_KEY")

# Store your Notion website URL here, Change xxx to your notion domain
website = f"https://xxx.notion.site/xxx-{page_id}"

# System used
if re.match(r"^[A-Za-z]\:", os.getcwd()):
    system_used = "Windows"
elif re.match(r"^/Users", os.getcwd()):
    system_used = "Mac"

# root is the folder that you store your CV and outputs
root = "../"
download_folder = f"{root}/Cover Letter"
cv_folder = f"{root}/CV"
package_folder = f"{root}/Package"

# Chromedriver path
binary_location = (
    "C:/Program Files/chrome-win32/chrome.exe"
    if system_used == "Windows"
    else "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)
path_to_chromedriver = (
    "./tools/chromedriver-win64/chromedriver.exe"
    if system_used == "Windows"
    else "./tools/chromedriver-mac-arm64/chromedriver"
)

cv_dict = {}  # Fetch correct CV by key input
cv_location_dict = {}  # Fetch correct CV location by key input

# Append your CVs in this format, you can also change alias of a certain CV
# CV1: CV for data science roles
cv_ds = """

"""
cv_dict["data_science"] = cv_ds
cv_location_dict["data_science"] = f"{cv_folder}/cv_ds.pdf"

# CV2: CV for software engineering roles
cv_swe = """

"""
cv_dict["software_engineering"] = cv_swe
cv_location_dict["software_engineering"] = f"{cv_folder}/cv_swe.pdf"

# CV3: CV for product management roles
cv_pm = """

"""
cv_dict["product_management"] = cv_pm
cv_location_dict["product_management"] = f"{cv_folder}/cv_pm.pdf"


# Supplemental Data
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
