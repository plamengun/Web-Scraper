import json
import re
from common.models import Job_Application, Job_Posting_Qualifier
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


def extract_data_from_xml(job_post):
    xml_to_str = job_post.description.text
    posted_on = match_re_pattern(POSTED_ON_PATTERN, xml_to_str)
    return posted_on


def create_job_application(job_posting_description_data: str) -> Job_Application:
    job_application =  Job_Application(job_posting_description=job_posting_description_data)
    return job_application


def create_job_posting_qualifier(job_posting_data: tuple, client_info_data: str) -> Job_Posting_Qualifier:
    job_posting_qualifier = Job_Posting_Qualifier(title=job_posting_data[0], 
                                                  url=job_posting_data[1], 
                                                  description=job_posting_data[2],
                                                  posted_before=job_posting_data[3], 
                                                  connects_required=job_posting_data[4],
                                                  connects_available=job_posting_data[5],
                                                  client_country=job_posting_data[6],
                                                  application_page_url=job_posting_data[7],
                                                  client_properties=client_info_data)
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