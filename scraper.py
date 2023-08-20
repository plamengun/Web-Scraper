from bs4 import BeautifulSoup
import requests
from browser_controller import pw_login
import json


PATH = 'common/storage.py'

with open(PATH, 'r') as file:
    open_storage = json.load(file)


def extract_job_posts(pages: list[str]):
    job_dict = {}
    
    for page in pages:

        resp_url = requests.get(f"{page}")
        soup = BeautifulSoup(resp_url.content, 'xml')
        job_posts = soup.find_all('item')

        for job_post in job_posts:
            if job_post.title.text not in open_storage:
                title = job_post.title.text
                url = job_post.link.text
                job_dict[title] = [url]

    with open(PATH, 'a') as file:
        file.write(json.dumps(job_dict, sort_keys=False, indent=4))
    
    return job_dict


if __name__ == "__main__":
    pages_to_extract = pw_login()
    print(extract_job_posts(pages_to_extract))