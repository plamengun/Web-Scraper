import json
import re
from scrape_runs.models import JobPostingQualifier, JobApplication
from logic.services.gpt import askgpt
from logic.common.vars import ROLE_QUALIFY_PROMPT, ROLE_APPLY_PROMPT


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


def create_job_application(job_posting_description_data: str) -> JobApplication:
    job_application =  JobApplication(job_posting_description=job_posting_description_data)
    return job_application


def create_job_posting_qualifier(job_posting_data: tuple, client_info_data: str) -> JobPostingQualifier:
    job_posting_qualifier = JobPostingQualifier()
    job_posting_qualifier.title=job_posting_data[0], 
    job_posting_qualifier.url=job_posting_data[1], 
    job_posting_qualifier.description=job_posting_data[2],
    job_posting_qualifier.posted_before=job_posting_data[3], 
    job_posting_qualifier.connects_required=job_posting_data[4],
    job_posting_qualifier.connects_available=job_posting_data[5],
    job_posting_qualifier.client_country=job_posting_data[6],
    job_posting_qualifier.application_page_url=job_posting_data[7],
    job_posting_qualifier.client_properties=client_info_data
    return job_posting_qualifier


def get_gpt_answers_apply(job_application: JobApplication) -> list[str]:
    job_application.add_description_to_questions()
    chat_log = askgpt(ROLE_APPLY_PROMPT, job_application.question_texts)
    job_application.chat_log = chat_log
    answers = job_application.answer_texts
    return answers


def get_gpt_answers_qualify(job_posting_qualifier: JobPostingQualifier):
    client_properties_list = [job_posting_qualifier.convert_to_str()]
    chat_log = askgpt(ROLE_QUALIFY_PROMPT, client_properties_list)
    return chat_log