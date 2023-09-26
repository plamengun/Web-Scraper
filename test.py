from playwright.sync_api import sync_playwright, JSHandle
from common.models import Job_Application
from typing import List
from dotenv import load_dotenv
from common.utils import create_job_application, get_gpt_answers
import os
import re

load_dotenv()

# def pw_job_posting():
# print(pw_job_posting_scrape())


def calculate_connects(connects_required: int = 12, available_connects: int = 1) -> str | None:
    if available_connects - connects_required >= 0:
        return 'True'




job_post = 'https://www.upwork.com/ab/proposals/job/~01348565d6d5978545/apply/'

    
def pw_job_post_application_page_scrape(application_page_url):
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
        page.goto(application_page_url)

        questions_texts_list = []
        question_fields_list = []
        cover_letter_field = page.query_selector('//div[@class="cover-letter-area"]//textarea')
        description = page.query_selector(f"//div[@class='description']").text_content()

        if page.query_selector(f'//div[@class="fe-proposal-job-questions questions-area"]'):
            questions_elements = page.query_selector_all(f'//div[@class="fe-proposal-job-questions questions-area"]//label[@class="up-label"]')
            for element in questions_elements:
                text_content = element.text_content().strip()
                questions_texts_list.append(text_content)
            question_fields_list = page.query_selector_all(f'//div[@class="fe-proposal-job-questions questions-area"]//textarea')
            question_fields_list.insert(0, cover_letter_field)

        job_application = create_job_application(description)
        job_application.question_texts = questions_texts_list

        answers = get_gpt_answers(job_application)

        for i, element in enumerate((question_fields_list)):
            if i < len(answers):
                element.fill(answers[i])
        
        return questions_texts_list
    

print(pw_job_post_application_page_scrape(job_post))








def pw_job_post_apply(application_page_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        # context.add_cookies(session_data)
        page = context.new_page()

        page.goto(application_page_url)
        page.wait_for_event("load")
        # page.get_by_text("By project").click()
        # page.get_by_text('Select a duration').click()
        # page.get_by_text('1 to 3 months').click()
        # page.wait_for_event("load")
        # print('Success')
        
