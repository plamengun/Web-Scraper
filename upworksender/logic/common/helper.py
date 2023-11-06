import json
import re
from .database import get_scrape_run_by_id
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


async def extract_data_from_xml(job_post):
    xml_to_str = job_post.description.text
    posted_on = match_re_pattern(POSTED_ON_PATTERN, xml_to_str)
    return posted_on


async def create_job_application(job_posting_description_data: str) -> JobApplication:
    job_application = JobApplication(job_posting_description=job_posting_description_data)
    return job_application


async def create_job_posting_qualifier(job_posting_data: tuple, client_info_data: str) -> JobPostingQualifier:
    job_posting_qualifier = JobPostingQualifier()
    job_posting_qualifier.title=job_posting_data[0]
    job_posting_qualifier.url=job_posting_data[1]
    job_posting_qualifier.description=job_posting_data[2]
    job_posting_qualifier.posted_before=job_posting_data[3]
    job_posting_qualifier.connects_required=job_posting_data[4]
    job_posting_qualifier.connects_available=job_posting_data[5]
    job_posting_qualifier.client_country=job_posting_data[6]
    job_posting_qualifier.application_page_url=job_posting_data[7]
    job_posting_qualifier.client_properties=client_info_data
    return job_posting_qualifier


async def create_job_posting_qualifier_when_error(job_posting_qualifier: JobPostingQualifier | None, posted_on:str, title:str, url: str, scrape_run_id: int, error: str) -> JobPostingQualifier:
    if job_posting_qualifier is None:
        job_posting_qualifier = JobPostingQualifier()
    job_posting_qualifier.title=title
    job_posting_qualifier.url=url
    if job_posting_qualifier.description is None:
        job_posting_qualifier.description = 'NA'
    job_posting_qualifier.posted_before=posted_on, 
    if job_posting_qualifier.connects_required is None:
        job_posting_qualifier.connects_required = 999
    if job_posting_qualifier.connects_available is None:
        job_posting_qualifier.connects_available = 999
    if job_posting_qualifier.client_country is None:
        job_posting_qualifier.client_country = 'NA'
    if job_posting_qualifier.application_page_url is None:
        job_posting_qualifier.application_page_url = 'NA'
    if job_posting_qualifier.client_properties is None:
        job_posting_qualifier.client_properties = 'NA'
    job_posting_qualifier.scrape_run=await get_scrape_run_by_id(scrape_run_id)
    job_posting_qualifier.error=error
    return job_posting_qualifier



async def get_gpt_answers_apply(job_application: JobApplication) -> list[str]:
    await job_application.add_description_to_questions()
    #TODO  "error": "object NoneType can't be used in 'await' expression"
    chat_log = await askgpt(ROLE_APPLY_PROMPT, job_application.question_texts)
    #TODO returns an empty chat log WHY?
    job_application.chat_log = chat_log
    answers = job_application.answer_texts
    return answers


async def get_gpt_answers_qualify(job_posting_qualifier: JobPostingQualifier):
    client_properties_list = [job_posting_qualifier.convert_to_str()]
    chat_log = await askgpt(ROLE_QUALIFY_PROMPT, client_properties_list)
    return chat_log