from bs4 import BeautifulSoup
import requests
from browser_controller import pw_login
import json


def extract_job_posts(pages: list):
    job_dict = {}
    for page in pages:

        resp_url = requests.get(f"{page}")

        soup = BeautifulSoup(resp_url.content, 'xml')
        job_posts = soup.find_all('item')

        for job_post in job_posts:
            title = job_post.title.text
            url = job_post.link.text
            job_dict[title] = [url]
    
    return job_dict


def write_in_storage(job_posts):
    with open('common/storage.py', 'w') as file:
        json_job_dict = json.dumps(extract_job_posts(pw_login()), sort_keys=False, indent=4)
        file.write(json_job_dict)
        file.close()


def read_from_storage():
    with open('common/storage.py', 'r') as file:
        pass