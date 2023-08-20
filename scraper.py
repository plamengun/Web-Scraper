from bs4 import BeautifulSoup
import requests
from browser_controller import pw_login
import json


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

    
def extract_job_posts(pages: list[str]):
    job_dict = {}
    open_storage = load_storage()

    for page in pages:

        resp_url = requests.get(f"{page}")
        soup = BeautifulSoup(resp_url.content, 'xml')
        job_posts = soup.find_all('item')

        for job_post in job_posts:
            if job_post.title.text not in open_storage:
                title = job_post.title.text
                url = job_post.link.text
                job_dict[title] = [url]

    open_storage.update(job_dict)
    save_storage(open_storage)
    
    return job_dict


if __name__ == "__main__":
    pages_to_extract = pw_login()
    print(extract_job_posts(pages_to_extract))