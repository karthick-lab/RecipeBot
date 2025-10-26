from playwright.sync_api import sync_playwright
from modules.recipe_parser import parse_recipe
import time

def query_gemini(prompt):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True after login
        page = browser.new_page()

        # Go to Gemini
        page.goto("https://gemini.google.com/app")

        # Wait for login manually if needed
        if "Sign in" in page.content():
            print("⚠️ Please sign in to Gemini manually and rerun.")
            browser.close()
            return None

        # Wait for input box
        page.wait_for_selector("textarea", timeout=10000)

        # Type prompt and submit
        page.fill("textarea", prompt)
        page.keyboard.press("Enter")

        # Wait for response to load
        time.sleep(8)
        page.wait_for_selector("div.markdown", timeout=15000)

        # Extract response
        response = page.query_selector("div.markdown").inner_text()
        browser.close()

        return parse_recipe(response)