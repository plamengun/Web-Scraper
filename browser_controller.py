from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto('https://www.upwork.com/ab/account-security/login')
    page.fill('input#login_username', 'plamenmgunchev44@gmail.com')
    page.click('button#login_password_continue')
    page.fill('input#login_password', os.environ.get('UW_PASSWORD'))
    page.click('button#login_control_continue')
    page.wait_for_event('pageload')