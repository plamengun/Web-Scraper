from playwright.async_api import async_playwright
from logic.common.helper import create_job_application, get_gpt_answers_apply
from rest_framework.response import Response
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
        while n < 1:
            if self.page.wait_for_selector(f"//div[@data-test='UpCDropdownSecondary RssAtomLink']//div[@class='air3-dropdown-secondary']//button"):
                rss_feed_dropdown = self.page.locator(f"//div[@data-test='UpCDropdownSecondary RssAtomLink']//div[@class='air3-dropdown-secondary']//button")
                await rss_feed_dropdown.click()
            if self.page.get_by_text("RSS").is_visible():
                #TODO MAKE SURE YOU DONT HAVE FILTERS CONTAINING THE WORD RSS
                rss_feed_button = self.page.locator(f"text=RSS")
                rss_feed_button = rss_feed_button.nth(0)
            new_page_info = await self._new_page(rss_feed_button)
            new_page = await new_page_info.value
            rss_feeds.append(new_page.url)
            await new_page.close()
            await self.page.bring_to_front()
            if self.page.wait_for_selector(f"//button[@data-ev-label='pagination_next_page']"):
                next_button = self.page.locator(f"//button[@data-ev-label='pagination_next_page']")
                await next_button.click()
            n += 1
        return rss_feeds

    async def _new_page(self, button):
        async with self.context.expect_page() as new_page_info:
            await button.click()
        return new_page_info
    
    async def check_application_page_url(self, application_page_url: str) -> bool:
        if await self.page.locator(f"//div[@class='alert alert-danger']").is_visible():
            return print('Job post application page no longer available')
        if self.page.url != application_page_url:
            page = await self.context.new_page()
            await page.goto(application_page_url)
            self.page = page
            return False
        return True
    
    async def check_job_page_url(self, job_url: str) -> bool:
        if await self.page.locator(f"//div[@class='alert alert-danger']").is_visible():
            return print('Job post no longer available')
        if self.page != job_url:
            page = await self.context.new_page()
            await page.goto(job_url)
            self.page = page
            return False
        return True
    
    async def _check_if_text_element_exists(self, locator_str) -> str:
        if self.page.wait_for_selector(locator_str):
            element_str = await self.page.locator(locator_str).inner_text()
            return element_str
        raise ValueError(f'Element with path {locator_str} missing from page.')
    
    async def _check_if_text_elements_exist(self, locator_str) -> List[str]:
        if self.page.wait_for_selector(locator_str):
            elements_str = await self.page.locator(locator_str).all_inner_texts()
            return elements_str
        return ValueError(f'Elements with path {locator_str} missing from page.')
    
    async def _check_if_object_element_exists(self, locator_str: str) -> str:
        button = self.page.locator(locator_str)
        if button:
            return locator_str
        raise ValueError('Element not present on the page')
    
    async def _check_if_numeric_element_exists(self, locator_str) -> int | str:
        if self.page.wait_for_selector(locator_str):
            element_str = await self.page.locator(locator_str).inner_text()
            return int(re.findall(r'\d+', element_str)[0])
        raise ValueError(f'Element with path {locator_str} missing from page.')

    async def job_posting_scrape(self):
        description = await self._check_if_text_element_exists(f"//div[@data-test='Description']//p")
        connects_required = await self._check_if_numeric_element_exists(f"//div[@data-test='ConnectsAuction']/div[1]")
        connects_available = await self._check_if_numeric_element_exists(f"//div[@data-test='ConnectsAuction']/div[2]")
        posted_before_text = await self._check_if_text_element_exists(f"//div[@data-test='PostedOn']")
        client_country_text = await self._check_if_text_element_exists(f"//ul[@class='features text-light-on-muted list-unstyled mt-4']/li[@data-qa='client-location']/strong")
        apply_now_locator_str = await self._check_if_object_element_exists(f"//button[@aria-label='Apply Now']")
        application_page_url = await self._go_to_application_page(apply_now_locator_str)
        return description, posted_before_text, connects_required, connects_available, client_country_text, application_page_url

    async def _go_to_application_page(self, button_locator_str: str):
        await self.page.click(button_locator_str)
        await self.page.wait_for_event("load")
        application_page_url = self.page.url
        return application_page_url

    async def scrape_client_info(self) -> str:
        client_info_container = await self._check_if_text_elements_exist(f"//div[@data-test='AboutClientUser']")
        client_info_proposals = await self._check_if_text_elements_exist(f"//section[@data-test='ClientActivity']//ul")
        proposal_items = client_info_proposals[0].split("\n")
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
                #TODO elements not present on page
                await self.page.get_by_text('Select a frequency').click()
                await self.page.get_by_text('Never').click()
                return 'hour'
            if by_project:
                await self.page.get_by_text('Select a duration').click()
                await self.page.get_by_text('1 to 3 months').click()
                return 'project'
            else:
                return None
            

    async def job_posting_apply(self, description: str) -> str:
        #TODO make in try except block
        questions_texts_list = []
        question_fields_list = []
        cover_letter_field = await self.page.query_selector('//div[@class="cover-letter-area"]//textarea')

        #TODO Test https://www.upwork.com/ab/proposals/job/~0123c252110d541ad4/apply/ This postin has questions and is qualified

        if self.page.query_selector(f'//div[@class="fe-proposal-job-questions questions-area"]'):
            questions_elements = await self.page.query_selector_all(f'//div[@class="fe-proposal-job-questions questions-area"]//label[@class="up-label"]')
            for element in questions_elements:
                text_content = await element.text_content()
                text_content.strip()
                questions_texts_list.append(text_content)
            question_fields_list = await self.page.query_selector_all(f'//div[@class="fe-proposal-job-questions questions-area"]//textarea')
            question_fields_list.insert(0, cover_letter_field)

        job_application = await create_job_application(description)
        job_application.question_texts = questions_texts_list

        answers = await get_gpt_answers_apply(job_application)

        for i, element in enumerate((question_fields_list)):
            if i < len(answers):
                answer = answers[i].strip()
                await element.fill(answer)

        await self.check_application_page_type()
        
        send_button = self.page.locator(f"//footer[@class='pb-10 mt-20']/div/button[@class='up-btn up-btn-primary m-0']")
        
        await send_button.click()
        await self.page.wait_for_load_state("load")
        
        if self.page.locator(f"//div[@class='up-modal-content up-modal-headerless up-modal-desktop-container']"):
            accept_terms_button = self.page.locator(f"//div[@class='checkbox']//input[@name='checkbox']")
            await accept_terms_button.click()
            apply_button = self.page.locator(f"//div[@class='up-modal-footer']//button[@class='up-btn up-btn-primary m-0 btn-primary']")
            await apply_button.click()
            return 'Job Application Successful'
        elif self.page.get_by_text('Your proposal was submitted.'):
            return 'Job Application Successful'
        else:
            raise ValueError('Issue encountered during proposal sending!')

