from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os


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


def pw_job_posting(page, context):
    job_page = context.new_page()
    job_page.goto(page)
    


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
        page.close()
    return rss_feeds