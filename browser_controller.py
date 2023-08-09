from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

def rss_feed_extractor(page):
    n = 0
    while n < 5:
        rss_feed_dropdown = page.locator(f"//div[@id='rss-atom-links']")
        rss_feed_dropdown.click()
        rss_feed_button = page.locator(f"//div[@id='rss-atom-links']//span[@role='button' and normalize-space()='RSS']/span")
        rss_feed_button.click()
        new_page = page.wait_for_event('popup')
        new_page.bring_to_front()
        print(new_page.url)
        new_page.close()
        page.bring_to_front()
        page.wait_for_selector(f"//div[@class='up-card-footer pb-0 d-flex justify-space-between']//button[@class='up-pagination-item up-btn up-btn-link']", timeout=5000)
        next_button = page.locator(f"//div[@class='up-card-footer pb-0 d-flex justify-space-between']//button[@class='up-pagination-item up-btn up-btn-link']/div[@class='next-icon up-icon']")
        next_button.click()
        n += 1

#ToDo Look into how to implement it in Headless mode

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://www.upwork.com/ab/account-security/login')
    page.fill('input#login_username', 'plamenmgunchev44@gmail.com')
    page.click('button#login_password_continue')
    page.fill('input#login_password', os.environ.get('UW_PASSWORD'))
    page.click('button#login_control_continue')
    page.wait_for_event("load")
    anchor = page.locator(f"//div[@data-test='saved-searches']//span/a[@data-test-key='my_ideal_search']")
    anchor.click()
    page.wait_for_event("load")
    
    rss_feed_extractor(page)

    page.close()