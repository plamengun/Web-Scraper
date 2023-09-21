from playwright.sync_api import sync_playwright, JSHandle
from common.models import Job_Application
from typing import List
from dotenv import load_dotenv
import os
import re

load_dotenv()

# def pw_job_posting():
# print(pw_job_posting_scrape())


def calculate_connects(connects_required: int = 12, available_connects: int = 1) -> str | None:
    if available_connects - connects_required >= 0:
        return 'True'




job_post = 'https://www.upwork.com/ab/proposals/job/~0174eebd2faa73997b/apply/'

    

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
        


def pw_check_application_page_type(context):
    with context.expect_page() as new_page:
        by_milestone = new_page.locator("/fieldset[@id='milestoneMode']")
        by_hour = new_page.locator
        by_bid = ''

        if by_milestone.is_visible():
            pass


        if new_page.get_by_text("What is the full amount you'd like to bid for this job?"):
            pass



def pw_fill_in_cover_letter_and_questions(job_application: Job_Application, page):
    cover_letter = job_application.answer_texts.pop[0]
    answers = Job_Application.answer_texts
    page.fill(Job_Application.cover_letter_field, cover_letter)
    for i in range(len(answers)):
        page.fill(Job_Application.question_fields[i], answers[i])