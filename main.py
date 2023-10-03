from bs4 import BeautifulSoup
import requests
from services.browser_controller_service import UpworkScraper
from services.airtable_service import put_record_into_airtable
from common.utils import load_storage, save_storage, extract_data_from_xml, create_job_posting, create_job_posting_qualifier, get_gpt_answers_qualify



def driver(pages: list[str]):
    job_dict = {}
    open_storage = load_storage()

    for page in pages:

        resp_url = requests.get(f"{page}")
        soup = BeautifulSoup(resp_url.content, 'xml')
        job_posts = soup.find_all('item')

        for job_post in job_posts:
            if job_post.title.text not in open_storage:
                #extract data for the job posting
                posted_on = extract_data_from_xml(job_post)
                title = job_post.title.text
                url = job_post.link.text
                scraper.check_job_page_url(url)
                #TODO CHECK IF JOB POSTING PAGE WILL OPEN OR JOB NOT AVAILABLE
                client_info_data = scraper.scrape_client_info()
                job_post_data = scraper.job_posting_scrape()
                #create JobPosting object
                job_posting = create_job_posting(title, url, job_post_data)
                job_posting_qualifier = create_job_posting_qualifier(job_posting, client_info_data)
                #qualify job posting
                qualify_gpt_answers = get_gpt_answers_qualify(job_posting_qualifier)
                job_posting_qualifier.gpt_response = qualify_gpt_answers
                job_posting_qualifier_asnwer = job_posting_qualifier.parse_gpt_response()
                job_posting_qualifier.gpt_answer = job_posting_qualifier_asnwer
                job_posting_qualifier_answer = job_posting_qualifier.check_gpt_answer()
                print(job_posting_qualifier_answer)
                #TODO omit this convert_to_json at this step. for testing only
                print(job_posting_qualifier.convert_to_json())
                #apply to job posting
                if job_posting.check_available_connects() and job_posting_qualifier_answer:
                    scraper.check_application_page_url(job_posting.application_page_url)
                    print(scraper.job_posting_apply())
                    job_posting_qualifier.status = 'Applied'
                    print(put_record_into_airtable(job_posting_qualifier.convert_to_json()))
                else:
                    print(put_record_into_airtable(job_posting_qualifier.convert_to_json()))

                job_dict[title] = [url, job_posting.description, posted_on]
                open_storage.update(job_dict)
                save_storage(open_storage)
    
    return job_dict


if __name__ == "__main__":

    scraper = UpworkScraper()
    scraper.login()
    rss_feed = scraper.rss_feed_scrape()

    print(driver(rss_feed))