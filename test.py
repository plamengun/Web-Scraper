from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from common.variables import APPLY_PROMPT
from pydantic import BaseModel
from typing import List
from common.variables import *
import os
from services.gpt_requests_service import askgpt


load_dotenv()


# insert into scrape_runs_scraperun(id, start_time, finish_time, user_id)
# values(1, '2023-10-11 13:34', '2023-10-11 13:34', 1);

# select * from scrape_runs_scraperun;
# select * from scrape_runs_jobpostingqualifier;

def test_func(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        page = context.new_page()
        page.goto('https://www.upwork.com/ab/account-security/login')
        page.fill('input#login_username', os.environ.get('UW_EMAIL'))
        page.click('button#login_password_continue')
        page.fill('input#login_password', os.environ.get('UW_PASSWORD'))
        page.click('button#login_control_continue')
        page.wait_for_event("load")

        page.goto(url)
        description = page.query_selector(f"//div[@data-test='Description']//p").text_content()
        if description:
            print(description)
        else:
            print(False)

        page.close()
        context.close()
        browser.close()


if __name__ == '__main__':
    # Specify the URL you want to open in the Playwright context
    url = 'https://www.upwork.com/jobs/~010b00bc6e0e37eabf'


test_func(url)