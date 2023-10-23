from playwright.async_api import async_playwright
from logic.common.helper import create_job_application, get_gpt_answers_apply
from dotenv import load_dotenv
from typing import List
import os
import re

load_dotenv()

class UpworkScraper:
    def __init__(self):
        self.pw_instance = None
        self.context = None
        self.browser = None    
        self.page = None


    async def _start_pw_instance_and_browser(self):
        pw_instance = await async_playwright().start()
        self.browser = await pw_instance.chromium.launch(headless=False, slow_mo=50)
        self.pw_instance = pw_instance

    async def close_browser(self):
        if self.browser:
            await self.browser.close()
            self.browser = None

    async def close_instance(self):
        if self.pw_instance:
            await self.pw_instance.stop()
            self.pw_instance = None

    async def close_context(self):
        if self.context:
            await self.context.close()
            self.context = None

    async def login(self):
        await self._start_pw_instance_and_browser()

        context = await self.browser.new_context()
        page = await context.new_page()
        await page.goto('https://www.upwork.com/ab/account-security/login')
        await page.fill('input#login_username', os.environ.get('UW_EMAIL'))
        await page.click('button#login_password_continue')
        await page.fill('input#login_password', os.environ.get('UW_PASSWORD'))
        await page.click('button#login_control_continue')
        await page.wait_for_event("load")
        anchor = page.locator(f"//div[@data-test='saved-searches']//span/a[@data-test-key='my_ideal_search']")
        await anchor.click()
        await page.wait_for_event("load")

        self.context = context
        self.page = page
        return 'Login Successful'

    async def rss_feed_scrape(self):
        n = 0
        rss_feeds = []
        #TODO refactor to click on expand page instead of looping
        while n < 1:
            rss_feed_dropdown = self.page.locator(f"//div[@id='rss-atom-links']")
            await rss_feed_dropdown.click()
            rss_feed_button = self.page.locator(f"//div[@id='rss-atom-links']//span[@role='button' and normalize-space()='RSS']/span")
            new_page_info = await self._new_page(rss_feed_button)
            new_page = new_page_info.value
            await new_page.wait_for_load_state()
            await new_page.bring_to_front()
            rss_feeds.append(new_page.url)
            await new_page.close()
            await self.page.bring_to_front()
            await self.page.wait_for_selector(f"//div[@class='up-card-footer pb-0 d-flex justify-space-between']//button[@class='up-pagination-item up-btn up-btn-link']", timeout=5000)
            next_button = self.page.locator(f"//div[@class='up-card-footer pb-0 d-flex justify-space-between']//button[@class='up-pagination-item up-btn up-btn-link']/div[@class='next-icon up-icon']")
            await next_button.click()
            n += 1
        return rss_feeds

    async def _new_page(self, button):
        with self.context.expect_page() as new_page_info:
            await button.click()
        return new_page_info
    
    async def check_application_page_url(self, application_page_url: str) -> bool:
        if self.page.url != application_page_url:
            page = await self.context.new_page()
            await page.goto(application_page_url)
            self.page = page
            return False
        return True
    
    async def check_job_page_url(self, job_url: str) -> bool:
        if self.page != job_url:
            page = await self.context.new_page()
            await page.goto(job_url)
            self.page = page
            return False
        return True
    
    async def _check_if_text_element_exists(self, element) -> str:
        if element:
            return await element.inner_text()
        return 'None'
    
    async def _check_if_text_elements_exist(self, elements) -> List[str]:
        if elements:
            return await elements.all_inner_texts()
        return 'None'
    
    async def _check_if_object_element_exists(self, locator_str: str) -> str:
        button = self.page.locator(locator_str)
        if button:
            return locator_str
        raise ValueError('Element not present on the page')
    
    async def _check_if_numeric_element_exists(self, element) -> int | str:
        if element:
            text = await element.inner_text()
            return int(re.findall(r'\d+', text)[0])
        return 'None'

    async def job_posting_scrape(self):
        description = await self._check_if_text_element_exists(self.page.query_selector(f'//div[@data-test="description"]/div'))
        connects_required = await self._check_if_numeric_element_exists(self.page.query_selector(f'//div[@data-test="connects-auction"]/div'))
        connects_available = await self._check_if_numeric_element_exists(self.page.query_selector(f'//div[@data-test="connects-auction"]/div[@class="mt-10"]'))
        posted_before_text = await self._check_if_text_element_exists(self.page.query_selector(f'//div[@id="posted-on"]//span[@class]/span'))
        client_country_text = await self._check_if_text_element_exists(self.page.query_selector(f'//ul[@class="list-unstyled cfe-ui-job-about-client-visitor m-0-bottom"]/li[@data-qa="client-location"]/strong'))
        apply_now_locator_str = await self._check_if_object_element_exists(f'//button[@aria-label="Apply Now"]')
        application_page_url = await self._go_to_application_page(apply_now_locator_str)
        return description, posted_before_text, connects_required, connects_available, client_country_text, application_page_url

    
    async def _go_to_application_page(self, button_locator_str: str):
        await self.page.click(button_locator_str)
        await self.page.wait_for_event("load")
        application_page_url = self.page.url
        return application_page_url

    async def scrape_client_info(self) -> str:
        client_info_container = await self._check_if_text_elements_exist(self.page.locator(f"//div[@class='col-12 job-details-sidebar d-none d-lg-flex']//div[@data-testid='about-client-container']"))
        client_info_proposals = await self._check_if_text_elements_exist(self.page.locator(f"//div[@data-test='client-activity']//ul[@class='list-unstyled']"))
        proposal_items = client_info_proposals[0].split("\n")
        #TODO potentially pass all proposal items
        proposal_items_clean = [item.strip() for item in proposal_items]
        proposal_str = proposal_items_clean[0] + proposal_items_clean[1]
        items = client_info_container[0].split("\n")
        items_clean = [item.strip() for item in items]
        items_str = "\n".join(items_clean)
        items_final = f'''Job post has the following properties:\n{items_str} + \n{proposal_str}'''
        return items_final
    

    async def check_application_page_type(self):
            by_milestone = await self.page.get_by_text("How do you want to be paid?").is_visible()
            by_hour = await self.page.get_by_text("What is the rate you'd like to bid for this job?").is_visible()
            by_project = await self.page.get_by_text("What is the full amount you'd like to bid for this job?").is_visible()
            if by_milestone:
                await self.page.get_by_text("By project").click()
                await self.page.get_by_text('Select a duration').click()
                await self.page.get_by_text('1 to 3 months').click()
                return 'milestone'
            if by_hour:
                #TODO Check if this option is on page. If not apply.Example of job: https://www.upwork.com/ab/proposals/job/~0151606201566a3c9f/apply/
                await self.page.get_by_text('Select a duration').click()
                await self.page.get_by_text('1 to 3 months').click()
                return 'hour'
            if by_project:
                await self.page.get_by_text('Select a duration').click()
                await self.page.get_by_text('1 to 3 months').click()
                return 'project'
            else:
                return None


    async def job_posting_apply(self) -> str:
        #TODO make in try except block
        #TODO check success page after submission

        self.check_application_page_url(self.page.url)
        questions_texts_list = []
        question_fields_list = []
        cover_letter_field = await self.page.query_selector('//div[@class="cover-letter-area"]//textarea')
        #TODO AttributeError: 'NoneType' object has no attribute 'text_content' -> if this then take description from Job object
        description = await self.page.query_selector(f"//div[@class='description']").text_content()

        if await self.page.query_selector(f'//div[@class="fe-proposal-job-questions questions-area"]'):
            questions_elements = await self.page.query_selector_all(f'//div[@class="fe-proposal-job-questions questions-area"]//label[@class="up-label"]')
            for element in questions_elements:
                text_content = await element.text_content().strip()
                questions_texts_list.append(text_content)
            question_fields_list = await self.page.query_selector_all(f'//div[@class="fe-proposal-job-questions questions-area"]//textarea')
            question_fields_list.insert(0, cover_letter_field)

        job_application = create_job_application(description)
        job_application.question_texts = questions_texts_list

        answers = get_gpt_answers_apply(job_application)

        for i, element in enumerate((question_fields_list)):
            if i < len(answers):
                answer = answers[i].strip()
                element.fill(answer)

        await self.check_application_page_type()
        
        send_button = await self.page.locator(f"//footer[@class='pb-10 mt-20']/div/button[@class='up-btn up-btn-primary m-0']")
        await send_button.click()
        await self.page.wait_for_load_state("load")

        #ToDo Final Popup Menu
        popup = self.page.locator(f"//div[@class='up-modal-content up-modal-headerless up-modal-desktop-container']")
        if popup:
            accept_terms_button = await self.page.locator(f"//div[@class='checkbox']//input[@name='checkbox']")
            await accept_terms_button.click()
            apply_button = await self.page.locator(f"//div[@class='up-modal-footer']//button[@class='up-btn up-btn-primary m-0 btn-primary']")
            await apply_button.click()

            return 'Job Application Successful'

