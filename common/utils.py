import json
import re
from common.models import Job_Posting


PATH = 'common/storage.py'
POSTED_ON_PATTERN = r'<b>Posted On<\/b>: (.*?)<br \/>'


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


def extract_data_from_xml(job_post):
    xml_to_str = job_post.description.text
    posted_on = match_re_pattern(POSTED_ON_PATTERN, xml_to_str)
    return posted_on


def unpack_job_post_data(title: str, url: str, job_post_data: tuple) -> Job_Posting:
    title = title
    url = url
    posted_before, description, connects_required, connects_available, client_country = job_post_data
    job_posting = Job_Posting(title, url, posted_before, description, connects_required, connects_available, client_country)
    return job_posting