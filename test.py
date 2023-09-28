from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os


load_dotenv()


def calculate_connects(connects_required: int = 12, available_connects: int = 1) -> str | None:
    if available_connects - connects_required >= 0:
        return 'True'



application_page_url = 'https://www.upwork.com/jobs/Create-huggingface-dataset_~01d264e91c09c5a3f4/?referrer_url_path=find_work_home'
application_page_url1 = 'https://www.upwork.com/jobs/Cold-Message-Chat-Sales-Representative_~01568e95d9171986cd/?referrer_url_path=find_work_home'

def scrape_client_info(job_posting_details_url: str):
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
        page.goto(job_posting_details_url)

        client_info_container = page.locator(f"//div[@class='col-12 job-details-sidebar d-none d-lg-flex']//div[@data-testid='about-client-container']").all_inner_texts()
        items = client_info_container[0].split("\n")
        items_clean = [item.strip() for item in items]
        items_st = "\n".join(items_clean)
        items_final = f'''Job post has the following properties:\n{items_st}'''
        
        return [items_final]

# print(scrape_client_info(application_page_url1))



        # payment_verified = page.locator(f"//div[@class='col-12 job-details-sidebar d-none d-lg-flex']//div[@data-testid='about-client-container']//div[@class='mb-10']")
        # print(payment_verified.all_inner_texts())
        # reviews = page.locator(f"//div[@class='col-12 job-details-sidebar d-none d-lg-flex']//div[@data-testid='about-client-container']//div[@class='text-muted rating mb-20']")
        # print(reviews.all_inner_texts())
        # all_info = page.query_selector_all(f"//div[@class='col-12 job-details-sidebar d-none d-lg-flex']//div[@data-testid='about-client-container']//ul[@data-test='about-client-visitor']//li")
        # print(all_info)

        # jobs_posted = ''
        # total_spend = ''
        # avrg_hourly_rate = ''
        # member_since = ''
        # applications = ''




        
JOB_PROPERTIES = """Job post has the following properties:\nAbout the client\nPayment method verified\nRating is 4.581980441 out of 5.\n4.58 of 67 reviews\nUnited Arab Emirates\nDubai 5:55 pm\n135 jobs posted\n73% hire rate, 1 open 
job\n$93K total spent\n133 hires, 27 active\n$9.75 /hr avg hourly rate paid\n2,666 hours\nSales & Marketing\nMid-sized company (10-99 people)\nMember since Feb 21, 2019"""


print(JOB_PROPERTIES)