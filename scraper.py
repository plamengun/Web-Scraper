from bs4 import BeautifulSoup
import requests
from browser_controller import pw_login, pw_job_posting_scrape, pw_job_post_application_page_scrape
from common.utils import load_storage, save_storage, extract_data_from_xml, unpack_job_post_data


def extract_job_posts(pages: list[str], session_data):
    job_dict = {}
    open_storage = load_storage()

    for page in pages:

        resp_url = requests.get(f"{page}")
        soup = BeautifulSoup(resp_url.content, 'xml')
        job_posts = soup.find_all('item')

        for job_post in job_posts:
            if job_post.title.text not in open_storage:
                posted_on = extract_data_from_xml(job_post)
                title = job_post.title.text
                url = job_post.link.text
                job_post_data = pw_job_posting_scrape(url, session_data)
                job_posting = unpack_job_post_data(title, url, job_post_data)
                job_post_application_page_data = pw_job_post_application_page_scrape(job_posting.application_page_url, session_data)
                job_dict[title] = [url, job_posting.description, posted_on]
    open_storage.update(job_dict)
    save_storage(open_storage)
    
    return job_dict


if __name__ == "__main__":
    pages_to_extract, session_data = pw_login()
    print(extract_job_posts(pages_to_extract, session_data))