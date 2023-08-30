from playwright.sync_api import sync_playwright, JSHandle
from dotenv import load_dotenv
import os
from typing import List
import re


load_dotenv()


def pw_new_page(context, button):
    with context.expect_page() as new_page_info:
        button.click()
        return new_page_info


def pw_rss_feed_extractor(page, context):
    n = 0
    rss_feeds = []
    while n < 1:
        rss_feed_dropdown = page.locator(f"//div[@id='rss-atom-links']")
        rss_feed_dropdown.click()
        rss_feed_button = page.locator(f"//div[@id='rss-atom-links']//span[@role='button' and normalize-space()='RSS']/span")
        new_page_info = pw_new_page(context, rss_feed_button)
        new_page = new_page_info.value
        new_page.wait_for_load_state()    
        new_page.bring_to_front()
        rss_feeds.append(new_page.url)
        new_page.close()
        page.bring_to_front()
        page.wait_for_selector(f"//div[@class='up-card-footer pb-0 d-flex justify-space-between']//button[@class='up-pagination-item up-btn up-btn-link']", timeout=5000)
        next_button = page.locator(f"//div[@class='up-card-footer pb-0 d-flex justify-space-between']//button[@class='up-pagination-item up-btn up-btn-link']/div[@class='next-icon up-icon']")
        next_button.click()
        n += 1
    return rss_feeds


def pw_job_posting_scrape(job_url, session_data):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        context.add_cookies(session_data)
        page = context.new_page()

        page.goto(job_url)
        description = page.query_selector(f'//div[@data-test="description"]/div').inner_text()
        connects_required_text = page.query_selector(f'//div[@data-test="connects-auction"]/div').inner_text()
        connects_required = int(re.findall(r'\d+', connects_required_text)[0])
        available_connects_text = page.query_selector(f'//div[@data-test="connects-auction"]/div[@class="mt-10"]').inner_text()
        available_connects = int(re.findall(r'\d+', available_connects_text)[0])
        posted_on_text = page.query_selector(f'//div[@id="posted-on"]//span[@class]/span').inner_text()
        client_country_text = page.query_selector(f'//ul[@class = "list-unstyled cfe-ui-job-about-client-visitor m-0-bottom"]/li[@data-qa="client-location"]/strong').inner_text()
        page.click('//button[@aria-label="Apply Now"]')
        page.wait_for_event("load")
        context.close()
    return description, connects_required, available_connects, posted_on_text, client_country_text


def pw_login():
    # This is the driver function.

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
        anchor = page.locator(f"//div[@data-test='saved-searches']//span/a[@data-test-key='my_ideal_search']")
        anchor.click()
        page.wait_for_event("load")
        rss_feeds = pw_rss_feed_extractor(page, context)
        session_data = context.cookies()
        context.close()
    return rss_feeds, session_data