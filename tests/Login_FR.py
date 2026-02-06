import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://production.sureprep.com/home/PreLogin")
    page.get_by_role("link", name="Sign in with Thomson Reuters").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("Priyanka.Patil@thomsonreuters.com")
  
    page.goto("https://production.sureprep.com/Ciam/AuthenticateCiamUser")
    page.get_by_label("Select Firm ID").select_option("7061501")
    page.get_by_role("button", name="Submit").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Product Dropdown").click()
    page.locator("html").click()
    page.get_by_role("menuitem", name="Admin").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
