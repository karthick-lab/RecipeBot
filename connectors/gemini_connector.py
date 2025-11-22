import json
import os
import sys

from playwright.sync_api import sync_playwright
from modules.recipe_parser import parse_gemini_response
import time

# Start Playwright manually
playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)
page = browser.new_page()

exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
config_file = os.path.join(exe_dir, "config.json")

with open(config_file, "r") as f:
    CONFIG = json.load(f)

def query_gemini(prompt):
    page.goto(CONFIG["gemini_model"])

    page.wait_for_selector("xpath=//*[@class='ql-editor ql-blank textarea new-input-ui']", timeout=15000)
    page.locator("xpath=//*[@class='ql-editor ql-blank textarea new-input-ui']").fill(prompt)
    print("✅ Prompt entered")

    page.wait_for_selector("xpath=//*[contains(@class,'mat-mdc-tooltip-trigger send-button-container')]", timeout=10000)
    page.locator("xpath=//*[contains(@class,'mat-mdc-tooltip-trigger send-button-container')]").click()
    print("✅ Prompt sent")

    time.sleep(8)
    page.wait_for_selector("xpath=//div[contains(@class,'markdown')]", timeout=15000)
    response = page.locator("xpath=//div[contains(@class,'markdown')]").inner_text()
    print("✅ Response received")
    print("🧾 Full model response:\n", response)

    return response