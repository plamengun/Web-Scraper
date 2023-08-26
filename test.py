from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import re


load_dotenv()


# def pw_job_posting():


def pw_login():

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

        page = context.new_page()
        page.goto("https://www.upwork.com/jobs/~018842df85fdf63512")
        description = page.query_selector(f'//div[@data-test="description"]/div').inner_text()
        connects_required_text = page.query_selector(f'//div[@data-test="connects-auction"]/div').inner_text()
        connects_required = int(re.findall(r'\d+', connects_required_text)[0])
        available_connects_text = page.query_selector(f'//div[@data-test="connects-auction"]/div[@class="mt-10"]').inner_text()
        available_connects = int(re.findall(r'\d+', available_connects_text)[0])
        posted_on_text = page.query_selector(f'//div[@id="posted-on"]//span[@class]/span').inner_text()
        client_location_text = page.query_selector(f'//ul[@class = "list-unstyled cfe-ui-job-about-client-visitor m-0-bottom"]/li[@data-qa="client-location"]/strong').inner_text()
        page.click('//button[@aria-label="Apply Now"]')
        page.wait_for_event("load")

        page.close()
        context.close()

    return description, connects_required, available_connects, posted_on_text, client_location_text

print(pw_login())


def calculate_connects(connects_required: int = 12, available_connects: int = 1) -> str | None:
    if available_connects - connects_required >= 0:
        return 'True'