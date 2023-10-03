import json
import re
from common.models import Job_Posting, Job_Application, Job_Posting_Qualifier
from common.variables import *
from services.gpt_requests_service import askgpt


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


def extract_data_from_xml(job_post: Job_Posting):
    xml_to_str = job_post.description.text
    posted_on = match_re_pattern(POSTED_ON_PATTERN, xml_to_str)
    return posted_on


def create_job_posting(title: str, url: str, job_post_data: tuple) -> Job_Posting:
    posted_before, description, connects_required, connects_available, client_country, application_page_url = job_post_data
    job_posting = Job_Posting(title=title, 
                              url=url, 
                              posted_before=posted_before, 
                              description=description, 
                              connects_required=connects_required, 
                              connects_available=connects_available, 
                              client_country=client_country, 
                              application_page_url=application_page_url)
    return job_posting


def create_job_application(job_posting_description: str) -> Job_Application:
    job_application =  Job_Application(job_posting_description)
    return job_application


def create_job_posting_qualifier(job_posting: Job_Posting, client_info_data: list[str]) -> Job_Posting_Qualifier:
    job_posting_qualifier = Job_Posting_Qualifier(job_posting.title, 
                                                  job_posting.url, 
                                                  job_posting.posted_before, 
                                                  job_posting.description, 
                                                  job_posting.connects_required,
                                                  job_posting.connects_available,
                                                  job_posting.client_country,
                                                  client_info_data)
    return job_posting_qualifier


def get_gpt_answers_apply(job_application: Job_Application) -> list[str]:
    job_application.add_description_to_questions()
    chat_log = askgpt(ROLE_APPLY_PROMPT, job_application.question_texts)
    job_application.chat_log = chat_log
    answers = job_application.answer_texts
    return answers


def get_gpt_answers_qualify(job_posting_qualifier: Job_Posting_Qualifier):
    client_properties_list = [job_posting_qualifier.convert_to_str()]
    chat_log = askgpt(ROLE_QUALIFY_PROMPT, client_properties_list)
    return chat_log