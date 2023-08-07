from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto('https://www.upwork.com/ab/account-security/login')
    page.fill('input#login_username', 'plamenmgunchev44@gmail.com')
    page.click('button#login_password_continue')
    page.fill('input#login_password', os.environ.get('UW_PASSWORD'))
    page.click('button#login_control_continue')
    page.wait_for_event("load")
    url = page.url
    anchor = page.locator(f"//div[@data-test='saved-searches']//span/a[@data-test-key='my_ideal_search']")
    anchor.click()
    page.wait_for_event("load")
    dropdown = page.locator(f"//div[@data-test='jobs_per_page']//div[@data-test='dropdown-toggle']")
    dropdown.click()

    option = dropdown.locator()
    option.click()
    page.wait_for_event("load")
    page.close()
    print(url)


