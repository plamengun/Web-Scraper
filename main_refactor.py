from bs4 import BeautifulSoup
import requests
from browser_controller_refactor import UpworkScraper
from common.utils import load_storage, save_storage, extract_data_from_xml, unpack_job_post_data, unpack_job_posting_application_page_data
from gpt_requests import askgpt


def driver(pages: list[str]):
    job_dict = {}
    open_storage = load_storage()

    for page in pages:

        resp_url = requests.get(f"{page}")
        soup = BeautifulSoup(resp_url.content, 'xml')
        job_posts = soup.find_all('item')

        for job_post in job_posts:
            if job_post.title.text not in open_storage:
                #Extract data for the job posting
                posted_on = extract_data_from_xml(job_post)
                title = job_post.title.text
                url = job_post.link.text
                scraper.check_job_page_url(url)
                job_post_data = scraper.job_posting_scrape()
                #Create JobPosting object
                job_posting = unpack_job_post_data(title, url, job_post_data)
                #Extract data from job posting application page
                #ToDO Test this
                scraper.check_application_page_url(job_posting.application_page_url)
                job_post_application_page_data = scraper.job_post_application_page_scrape()
                #Create JobApplication object
                job_application = unpack_job_posting_application_page_data(job_post_application_page_data, job_posting.description)
                job_application.add_description_to_questions()
                #Send JobApplication object to ChatGPT
                chat_log = askgpt(job_application.question_texts)
                #Update JobApplication object with answers from ChatGPT
                job_application.chat_log = chat_log
                answers = job_application.extract_answers_from_log()
                print(answers)
                #Save processed job posting in storage JSON
                job_dict[title] = [url, job_posting.description, posted_on]
    open_storage.update(job_dict)
    save_storage(open_storage)
    
    return job_dict


if __name__ == "__main__":

    scraper = UpworkScraper()
    scraper.login()
    rss_feed = scraper.rss_feed_scrape()

    print(driver(rss_feed))