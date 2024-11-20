import re
import os
import json
import time
import base64
import shutil
import PyPDF2
import requests
import pyperclip
import pdfplumber
import tkinter as tk

from cv_info import *
from config import notion_api_key

from glob import glob
from openai import OpenAI
from PyPDF2 import PdfMerger
from datetime import datetime
from tkinter import messagebox
from notion_client import Client

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def ready_for_chromedriver(binary_location, path_to_chromedriver):
    # Specify some options for the webdriver to avoid exceptions
    # Chromedriver: 113, Chrome: 113-32bits
    options = webdriver.ChromeOptions()
    options.binary_location = binary_location

    # options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "download.prompt_for_download": False,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
    }
    options.add_experimental_option("prefs", prefs)
    # options.add_argument("--headless=new")

    path_to_chromedriver = path_to_chromedriver

    # Initialize the webdriverchromedriver-win64
    service = Service()

    return path_to_chromedriver, service, options


def get_notion(api_key=notion_api_key):
    return Client(auth=api_key)


def parse_text(extracted_text):
    # Split by double new lines (paragraphs)
    paragraphs = extracted_text.split("\n\n")

    result = []
    for paragraph in paragraphs:
        # Process bold text within the paragraph
        parts = re.split(r"(\*\*.*?\*\*)", paragraph)

        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                result.append({"content": part[2:-2], "bold": True})
            else:
                result.append({"content": part, "bold": False})

        # Add a paragraph separator after each paragraph except the last one
        if paragraph != paragraphs[-1]:
            result.append({"content": "\n\n", "type": "new_block"})

    return result


def get_page_blocks(page_id):
    notion = get_notion()
    response = notion.blocks.children.list(block_id=page_id)
    return response["results"]


def find_block_by_text(blocks, search_text):
    notion = get_notion()
    for block in blocks:
        if block["type"] == "paragraph" and "rich_text" in block["paragraph"]:
            paragraph_text = "".join(
                [t["text"]["content"] for t in block["paragraph"]["rich_text"]]
            )
            if search_text in paragraph_text:
                return block["id"], paragraph_text
        elif block["type"] == "column_list":
            column_blocks = notion.blocks.children.list(block_id=block["id"])["results"]
            for column_block in column_blocks:
                if column_block["type"] == "column":
                    column_content = notion.blocks.children.list(
                        block_id=column_block["id"]
                    )["results"]
                    for sub_block in column_content:
                        if (
                            sub_block["type"] == "paragraph"
                            and "rich_text" in sub_block["paragraph"]
                        ):
                            sub_paragraph_text = "".join(
                                [
                                    t["text"]["content"]
                                    for t in sub_block["paragraph"]["rich_text"]
                                ]
                            )
                            if search_text in sub_paragraph_text:
                                return sub_block["id"], sub_paragraph_text
    return None, None


def update_block_content(block_id, text_segments, change_color=False, color_to=None):
    notion = get_notion()
    rich_text = [
        {
            "type": "text",
            "text": {"content": segment["content"]},
            "annotations": {"bold": segment.get("bold", False)},
        }
        for segment in text_segments
    ]

    if not change_color:
        notion.blocks.update(block_id=block_id, paragraph={"rich_text": rich_text})
        time.sleep(2)
        print(f"Block {block_id} updated.")
    else:
        notion.blocks.update(
            block_id=block_id, paragraph={"rich_text": rich_text, "color": color_to}
        )
        time.sleep(2)
        print(f"Block {block_id} updated with color '{color_to}'.")


def replace_simple(old_text, new_text, page_id, change_color=False, color_to=None):
    new_text = parse_text(new_text)

    blocks = get_page_blocks(page_id)
    block_id, found_text = find_block_by_text(blocks, old_text)

    if block_id:
        print(f"Found block with text: {found_text}")
        update_block_content(block_id, new_text, change_color, color_to)
    else:
        assert False, f"Text '{old_text}' not found in the page."

    return True, block_id


def check_TBA(driver):
    retry = 0
    while retry <= 3:
        try:
            body_text = driver.find_element(By.TAG_NAME, "body").text
            if "TBA" in body_text:
                print(f"TBA found on retry {retry}, refreshing the page...")
                driver.refresh()
                time.sleep(3)
                retry += 1
            else:
                print("No TBA found, page is successful.")
                return True
        except NoSuchElementException:
            raise Exception("Unable to find page body element.")

    body_text = driver.find_element(By.TAG_NAME, "body").text
    if "TBA" in body_text:
        raise Exception("Page contains 'TBA' after 3 retries, indicating an issue.")
    else:
        print("No TBA found after retries.")
        return True


def print_to_pdf(driver, file_path):
    print_options = {
        "scale": 0.83,  # 85% margin
        "paperWidth": 8.5,  # Letter width
        "paperHeight": 11,  # Letter height
        # 'marginTop': 0.4,
        # 'marginBottom': 0.4,
        # 'marginLeft': 0.4,
        # 'marginRight': 0.4,
        # 'printBackground': True,     # Print background graphics
        "preferCSSPageSize": True,  # Enable CSS page size preference
    }

    result = driver.execute_cdp_cmd("Page.printToPDF", print_options)

    with open(file_path, "wb") as f:
        f.write(base64.b64decode(result["data"]))

    print(f"PDF saved to {file_path}")


def selenium_download_pdf(service, options, download_folder, url):
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(5)
    driver.refresh()
    time.sleep(5)

    if check_TBA(driver):
        print("Page is successful, proceeding to download PDF.")

    print_to_pdf(driver, f"{download_folder}/Cover Letter - Fred Li.pdf")
    driver.quit()
    return True


def remove_blank_pages_from_pdf(input_pdf_path):
    with open(input_pdf_path, "rb") as file:
        pdf = PyPDF2.PdfReader(file)

        if len(pdf.pages) <= 1:
            print("Only one page in the PDF. No need to remove blank pages.")
            return

        with pdfplumber.open(input_pdf_path) as pdf_reader:
            first_page_text = pdf_reader.pages[0].extract_text()

            pages_to_keep = 1
            for i in range(1, len(pdf_reader.pages)):
                page_text = pdf_reader.pages[i].extract_text()

                if page_text and page_text.strip():
                    pages_to_keep = i + 1
                else:
                    print(f"Page {i + 1} is blank. Removing...")
                    break

        pdf_writer = PyPDF2.PdfWriter()

        with open(input_pdf_path, "rb") as file:
            pdf = PyPDF2.PdfReader(file)
            for page_num in range(pages_to_keep):
                pdf_writer.add_page(pdf.pages[page_num])

        with open(input_pdf_path, "wb") as output_file:
            pdf_writer.write(output_file)

        print(f"Saved PDF with {pages_to_keep} non-blank pages.")


def replace_text_in_blocks(blocks, start_text, end_text, replacement_text):
    in_replacement_section = False
    replacement_done = False

    notion = get_notion()
    for block in blocks:
        if block["type"] == "paragraph" and "rich_text" in block["paragraph"]:
            paragraph_text = "".join(
                [t["text"]["content"] for t in block["paragraph"]["rich_text"]]
            )

            if start_text in paragraph_text:
                in_replacement_section = True
                continue

            if end_text in paragraph_text and in_replacement_section:
                in_replacement_section = False
                replacement_done = True
                continue

            if in_replacement_section:
                update_block_content_2(block["id"], "")
                update_block_content_2(block["id"], replacement_text)
                replacement_done = True

        if block.get("has_children", False):
            child_blocks = notion.blocks.children.list(block_id=block["id"])["results"]
            replacement_done = (
                replace_text_in_blocks(
                    child_blocks, start_text, end_text, replacement_text
                )
                or replacement_done
            )

    return replacement_done


def update_block_content_2(block_id, new_text):
    notion = get_notion()
    notion.blocks.update(
        block_id=block_id,
        paragraph={"rich_text": [{"type": "text", "text": {"content": new_text}}]},
    )
    print(f"Updated block {block_id} with new text.")
    time.sleep(1)
