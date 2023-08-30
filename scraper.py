from bs4 import BeautifulSoup
import requests
from browser_controller import pw_login, pw_job_posting_scrape
from common.models import Job_Posting
import json
import re


PATH = 'common/storage.py'


def load_storage():
    try:
        with open(PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_storage(storage_data):
    with open(PATH, 'w') as file:
        json.dump(storage_data, file, sort_keys=False, indent=4)

    
def match_re_pattern(pattern, string: str) -> str:
    match_pattern = re.search(pattern, string, re.DOTALL | re.IGNORECASE)
    if match_pattern:
        final = match_pattern.group(1).strip()
    else:
        final = 'None'
    return final


def extract_job_posts(pages: list[str], session_data):
    job_dict = {}
    open_storage = load_storage()

    for page in pages:

        resp_url = requests.get(f"{page}")
        soup = BeautifulSoup(resp_url.content, 'xml')
        job_posts = soup.find_all('item')

        for job_post in job_posts:
            if job_post.title.text not in open_storage:
                xml_to_str = job_post.description.text
                posted_on_pattern = r'<b>Posted On<\/b>: (.*?)<br \/>'
                description_pattern = r'^(.*?)(?=<b>Posted)'

                title = job_post.title.text
                url = job_post.link.text
                posted_on = match_re_pattern(posted_on_pattern, xml_to_str)
                description = match_re_pattern(description_pattern, xml_to_str)
                job_post_data = pw_job_posting_scrape(url, session_data)
                job_posting = Job_Posting(title, url, posted_on, job_post_data[0], job_post_data[1], job_post_data[2], job_post_data[3])
                print(job_posting)
                job_dict[title] = [url, description, posted_on]

    open_storage.update(job_dict)
    save_storage(open_storage)
    
    return job_dict


if __name__ == "__main__":
    pages_to_extract, session_data = pw_login()
    print(extract_job_posts(pages_to_extract, session_data))