from bs4 import BeautifulSoup
import requests
from browser_controller_refactor import UpworkScraper
from common.utils import load_storage, save_storage, extract_data_from_xml, create_job_posting



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
                #TODO CHECK IF JOB POSTING PAGE WILL OPEN OR JOB NOT AVAILABLE
                job_post_data = scraper.job_posting_scrape()
                #Create JobPosting object
                job_posting = create_job_posting(title, url, job_post_data)
                #Extract data from job posting application page
                scraper.check_application_page_url(job_posting.application_page_url)
                print(scraper.job_posting_apply())
              

                job_dict[title] = [url, job_posting.description, posted_on]
                open_storage.update(job_dict)
                save_storage(open_storage)
    
    return job_dict


if __name__ == "__main__":

    scraper = UpworkScraper()
    scraper.login()
    rss_feed = scraper.rss_feed_scrape()

    print(driver(rss_feed))