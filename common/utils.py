import json
import re
import datetime
from common.models import Job_Posting, Job_Application
from services.gpt_requests_service import askgpt


PATH = 'common/storage.py'
POSTED_ON_PATTERN = r'<b>Posted On<\/b>: (.*?)<br \/>'


def get_current_datetime_as_string():
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")


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


def extract_data_from_xml(job_post: Job_Posting):
    xml_to_str = job_post.description.text
    posted_on = match_re_pattern(POSTED_ON_PATTERN, xml_to_str)
    return posted_on


def create_job_posting(title: str, url: str, job_post_data: tuple) -> Job_Posting:
    title = title
    url = url
    posted_before, description, connects_required, connects_available, client_country, application_page_url = job_post_data
    job_posting = Job_Posting(title, url, posted_before, description, connects_required, connects_available, client_country, application_page_url)
    return job_posting


def create_job_application(job_posting_description: str) -> Job_Application:
    job_application =  Job_Application(job_posting_description)
    return job_application


def get_gpt_answers(job_application: Job_Application) -> list[str]:
    
    job_application.add_description_to_questions()
    chat_log = askgpt(job_application.question_texts)
    job_application.chat_log = chat_log
    answers = job_application.answer_texts

    return answers