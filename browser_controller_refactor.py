from playwright.sync_api import sync_playwright
from common.utils import create_job_application, _get_gpt_answers
from dotenv import load_dotenv
import os
import re

load_dotenv()

class UpworkScraper:
    def __init__(self):
        self.pw_instance = None
        self.context = None
        self.browser = None    
        self.page = None


    def _start_pw_instance_and_browser(self):
        pw_instance = sync_playwright().start()
        self.browser = pw_instance.chromium.launch(headless=False, slow_mo=50)
        self.pw_instance = pw_instance

    def close_browser(self):
        if self.browser:
            self.browser.close()
            self.browser = None

    def close_instance(self):
        if self.pw_instance:
            self.pw_instance.stop()
            self.pw_instance = None

    def close_context(self):
        if self.context:
            self.context.close()
            self.context = None

    def login(self):
        self._start_pw_instance_and_browser()

        context = self.browser.new_context()
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

        self.context = context
        self.page = page
        return 'Login Successful'

    def rss_feed_scrape(self):
        n = 0
        rss_feeds = []
        while n < 1:
            rss_feed_dropdown = self.page.locator(f"//div[@id='rss-atom-links']")
            rss_feed_dropdown.click()
            rss_feed_button = self.page.locator(f"//div[@id='rss-atom-links']//span[@role='button' and normalize-space()='RSS']/span")
            new_page_info = self._new_page(rss_feed_button)
            new_page = new_page_info.value
            new_page.wait_for_load_state()
            new_page.bring_to_front()
            rss_feeds.append(new_page.url)
            new_page.close()
            self.page.bring_to_front()
            self.page.wait_for_selector(f"//div[@class='up-card-footer pb-0 d-flex justify-space-between']//button[@class='up-pagination-item up-btn up-btn-link']", timeout=5000)
            next_button = self.page.locator(f"//div[@class='up-card-footer pb-0 d-flex justify-space-between']//button[@class='up-pagination-item up-btn up-btn-link']/div[@class='next-icon up-icon']")
            next_button.click()
            n += 1
        return rss_feeds

    def _new_page(self, button):
        with self.context.expect_page() as new_page_info:
            button.click()
        return new_page_info
    
    def check_application_page_url(self, application_page_url: str):
        if self.page.url != application_page_url:
            page = self.context.new_page()
            page.goto(application_page_url)
            self.page = page
            return False
        return True
    
    def check_job_page_url(self, job_url):
        if self.page != job_url:
            page = self.context.new_page()
            page.goto(job_url)
            self.page = page
            return False
        return True
    
    def _check_if_text_element_exists(self, element) -> str:
        if element:
            return element.inner_text()
        return 'None'
    
    def _check_if_object_element_exists(self, locator_str):
        button = self.page.locator(locator_str)
        if button:
            return locator_str
        raise ValueError('Element not present on the page')
    
    def _check_if_numeric_element_exists(self, element) -> int | str:
        if element:
            text = element.inner_text()
            return int(re.findall(r'\d+', text)[0])
        return 'None'

    def job_posting_scrape(self):
        description = self._check_if_text_element_exists(self.page.query_selector(f'//div[@data-test="description"]/div'))
        connects_required = self._check_if_numeric_element_exists(self.page.query_selector(f'//div[@data-test="connects-auction"]/div'))
        available_connects = self._check_if_numeric_element_exists(self.page.query_selector(f'//div[@data-test="connects-auction"]/div[@class="mt-10"]'))
        posted_before_text = self._check_if_text_element_exists(self.page.query_selector(f'//div[@id="posted-on"]//span[@class]/span'))
        client_country_text = self._check_if_text_element_exists(self.page.query_selector(f'//ul[@class="list-unstyled cfe-ui-job-about-client-visitor m-0-bottom"]/li[@data-qa="client-location"]/strong'))
        apply_now_locator_str = self._check_if_object_element_exists(f'//button[@aria-label="Apply Now"]')
        application_page_url = self._go_to_application_page(apply_now_locator_str)
        return posted_before_text, description, connects_required, available_connects, client_country_text, application_page_url

    
    def _go_to_application_page(self, button_locator_str: str):
        self.page.click(button_locator_str)
        self.page.wait_for_event("load")
        application_page_url = self.page.url
        return application_page_url
    

    def check_application_page_type(self):
            by_milestone = self.page.locator("/fieldset[@id='milestoneMode']").is_visible()
            by_hour = self.page.get_by_text("What is the rate you'd like to bid for this job?").is_visible()
            by_project = self.page.get_by_text("What is the full amount you'd like to bid for this job?").is_visible()
            if by_milestone:
                self.page.get_by_text("By project").click()
                self.page.get_by_text('Select a duration').click()
                self.page.get_by_text('1 to 3 months').click()
                return 'milestone'
            if by_hour:
                self.page.get_by_text('Select a duration').click()
                self.page.get_by_text('1 to 3 months').click()
                return 'hour'
            if by_project:
                self.page.get_by_text('Select a duration').click()
                self.page.get_by_text('1 to 3 months').click()
                return 'project'
            else:
                return None


    def job_posting_apply(self):
        self.check_application_page_url(self.page.url)
        questions_texts_list = []
        question_fields_list = []
        cover_letter_field = self.page.query_selector('//div[@class="cover-letter-area"]//textarea')
        description = self.page.query_selector(f"//div[@class='description']").text_content()

        if self.page.query_selector(f'//div[@class="fe-proposal-job-questions questions-area"]'):
            questions_elements = self.page.query_selector_all(f'//div[@class="fe-proposal-job-questions questions-area"]//label[@class="up-label"]')
            for element in questions_elements:
                text_content = element.text_content().strip()
                questions_texts_list.append(text_content)
            question_fields_list = self.page.query_selector_all(f'//div[@class="fe-proposal-job-questions questions-area"]//textarea')
            question_fields_list.insert(0, cover_letter_field)

        job_application = create_job_application(description)
        job_application.question_texts = questions_texts_list

        answers = _get_gpt_answers(job_application)

        for i, element in enumerate((question_fields_list)):
            if i < len(answers):
                element.fill(answers[i])

        print(self.check_application_page_type())

        return 'Job Application Successful'

