# Project Name  
Auto Cover Letter Generator  

## Description
This project automates the process of using ChatGPT API to generate well-organized, highly-tailored Cover Letter during your job hunt. In this project, you are allowed to have multiple versions of CV, and let AI help you choose which CV to use based on what skillsets are required in Job Descriptions (JD).

## Features
- **CV Management**: Store and manage multiple versions of your CV
- **JD Analysis**: Extract key requirements and skills from job descriptions
- **Company Address Search Up**: Use Google Map API to automate the company address hunt process
- **CV-JD Matching**: AI-powered matching of CV versions to job requirements
- **Cover Letter Generation**: Automated creation of personalized cover letters using Notion API
- **API Integration**: Seamless interaction with ChatGPT API
- **Configuration Options**: Customize output format and style preferences
- **Centralized Storage of you Application History**: Keep track of all your job applications and generated cover letters in one place for easy reference and follow-up

## Before You Start
1. Set up API keys:
    - Get your own ChatGPT API, Notion API, and Google Map API Key
        - Get your ChatGPT API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
        - Get your Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
        - Create a new integration and get your Notion API key from [Notion Developers](https://www.notion.so/my-integrations)
    - Add your API keys:
      ```bash
      OPENAI_API_KEY=your_key_here
      GOOGLE_MAPS_API_KEY=your_key_here
      NOTION_API_KEY=your_key_here
      ```
    2. Setup your Notion Page:
        - Create a new page in Notion with placeholder blocks:
            - "TBA Title" for the cover letter title
            - "TBA Date" for the date
            - "TBA Address" for company address
            - "TBA Main Text" for the cover letter content
        - Connect the page to your integration:
            - Go to page settings
            - Click 'Connect to' and select your integration you just created
            - Confirm the connection
        - Publish the page:
            - Click 'Share' in the top right
            - Select 'Publish'
            - Copy and save the published page URL


## Installation
1. Clone this repository
2. Install required dependencies:
```bash
pip install -r python_packs.txt
```

## Configuration
Edit `config.py` to customize your settings:

### Personal Information
- Your Name
- Your One-sentence description

### API Configuration
- API keys and Notion Webpages
```bash
# Store your Notion page ID here
page_id = ""
# Store your ChatGPT API key here
api_key = ""
# Store your Notion API key here
notion_api_key = ""
# Store your Google Maps API key here
gmap_api_key = ""
# Store your Notion website URL here
website = f"https://fredhl.notion.site/Fred-H-Li-{page_id}"
```

### System Settings
- Operating System (Windows/macOS supported)
- Chrome Installation Path:
```bash
binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Windows example
binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # macOS example
```
- Chromedriver Path: The easiest way is to keep the tools folder in the cloned folder
```bash
chromedriver_path = "./tools/chromedriver-win64/chromedriver.exe"  # Windows example
chromedriver_path = "./tools/chromedriver-mac-arm64/chromedriver"  # macOS example
```

## Move Your Files
1. Upload your CV inside `configuration.py`
    - You can name your versions of CV as you wish
    - Update corresponding dictionaries `cv_dict` and `cv_location_dict` after pasting your CV as well
    ```bash
    cv_research = """
    TBA with your own version of CV
    """
    cv_dict["research"] = cv_research               # Append in cv_dict to get correct version of CV by calling "research"
    cv_location_dict["research"] = "research.pdf"   # Append in cv_location_dict by specifying CV pdf name in CV Folder
    
    cv_ibd = """
    Your own version of another version of CV
    """
    cv_dict["ibd"] = cv_ibd
    
    ```
3. Move Files:
    - Place CV PDF files in the `CV` folder according to `cv_location_dict` mapping
    - Place your unofficial transcript in the `Package` folder:
        ```
        Package/Unofficial Transcript - {Your name}.pdf
        ```

## Usage
1. Run the program:
    ```bash
    python main.ipynb
    ```

2. Prepare for execution:
    - Close any open PDF reader applications to avoid conflicts.

3. Input job application details:
    - Paste the job description.
    - Enter company name, city, and state **(required)**.
    - Select appropriate CV version:
        - If undecided, write:
            ```bash
            cv_type = "undecided"
            ```
            ChatGPT will help you choose and tell you the reason.
    - Add any relevant strengths to highlight.

4. Review outputs:
    - Check the generated cover letter in the Cover Letter folder.
    - Verify the application entry in `Application History.xlsx`.

*Note: Company address lookup is optional, but ensure no incorrect addresses from previous applications remain.*


## Contributing
1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support
For questions or issues, please open a GitHub issue, or contact me directly at fredhli@outlook.com

## Notes
- This project is a great opportunity to streamline your job application process and save valuable time.
- Don't hesitate to experiment with different CV versions and see which one works best for different job applications.
- Remember to keep your API keys secure and never share them publicly.
- Regularly update your CVs and cover letters to reflect your latest skills and experiences.
- If you encounter any issues, the community is here to help. Feel free to reach out!

Happy job hunting and best of luck!