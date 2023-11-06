from bs4 import BeautifulSoup
from rest_framework.response import Response
import requests
from logic.common.helper import create_job_posting_qualifier, extract_data_from_xml, get_gpt_answers_qualify, create_job_posting_qualifier_when_error
from logic.common.database import check_existing_job_posting, save_job_posting_qualifier
from logic.services.airtable import put_record_into_airtable
from logic.services.scraper import UpworkScraper


async def driver(pages: list[str], scraper: UpworkScraper, scrape_run_id: int):
    for page in pages:
        resp_url = requests.get(f"{page}")
        soup = BeautifulSoup(resp_url.content, 'xml')
        job_posts = soup.find_all('item')

        for job_post in job_posts:
            checked_post = await check_existing_job_posting(job_post.title.text)
            if checked_post is None:
                #extract data for the job posting
                try:
                    posted_on = await extract_data_from_xml(job_post)
                    title = job_post.title.text
                    url = job_post.link.text
                    await scraper.check_job_page_url()
                    #TODO CHECK IF JOB POSTING PAGE WILL OPEN OR JOB NOT AVAILABLE
                    client_info_data = await scraper.scrape_client_info()
                    job_post_data = await scraper.job_posting_scrape()
                    #create JobPosting object
                    packaged_data = (title, url) + job_post_data
                    # job_posting = create_job_posting(title, url, job_post_data)
                    job_posting_qualifier = await create_job_posting_qualifier(packaged_data, client_info_data)
                    #qualify job posting
                    qualify_gpt_answers = await get_gpt_answers_qualify(job_posting_qualifier)
                    job_posting_qualifier.gpt_response = qualify_gpt_answers
                    job_posting_qualifier_asnwer = job_posting_qualifier.parse_gpt_response()
                    job_posting_qualifier.gpt_answer = job_posting_qualifier_asnwer
                    job_posting_qualifier_answer = job_posting_qualifier.check_gpt_answer()
                    print(job_posting_qualifier_answer)
                    #TODO omit this convert_to_json at this step. for testing only
                    print(job_posting_qualifier.convert_to_json())
                    #apply to job posting
                    if job_posting_qualifier.check_available_connects() and job_posting_qualifier_answer:
                        await scraper.check_application_page_url(job_posting_qualifier.application_page_url[0])
                        await scraper.job_posting_apply(job_posting_qualifier.description[0])
                        job_posting_qualifier.status = 'Applied'
                        job_posting_qualifier.save()
                        print(put_record_into_airtable(job_posting_qualifier.convert_to_json()))
                    else:
                        print(put_record_into_airtable(job_posting_qualifier.convert_to_json()))
                        job_posting_qualifier.save()
                except Exception as e:
                    if 'job_posting_qualifier' in locals():
                        job_posting_qualifier_error = await create_job_posting_qualifier_when_error(job_posting_qualifier, posted_on, title, url, scrape_run_id, str(e))
                        await save_job_posting_qualifier(job_posting_qualifier_error)
                        return Response({'error': str(e)}, status=400)
                    job_posting_qualifier = None
                    job_posting_qualifier_error = await create_job_posting_qualifier_when_error(job_posting_qualifier, posted_on, title, url, scrape_run_id, str(e))
                    await save_job_posting_qualifier(job_posting_qualifier_error)
                    return Response({'error': str(e)}, status=400)