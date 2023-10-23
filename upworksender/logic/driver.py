from bs4 import BeautifulSoup
from django.http import JsonResponse
import requests
from logic.common.helper import create_job_posting_qualifier, extract_data_from_xml, get_gpt_answers_qualify
from logic.services.airtable import put_record_into_airtable
from logic.services.scraper import UpworkScraper


async def driver(pages: list[str], scraper: UpworkScraper):
    job_dict = {}
    for page in pages:
        resp_url = await requests.get(f"{page}")
        soup = await BeautifulSoup(resp_url.content, 'xml')
        job_posts = await soup.find_all('item')

        for job_post in job_posts:
            if job_post.title.text not in []:
                #extract data for the job posting
                posted_on = await extract_data_from_xml(job_post)
                title = await job_post.title.text
                url = await job_post.link.text

                await scraper.check_job_page_url(url)
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
                    await scraper.check_application_page_url(job_posting_qualifier.application_page_url)
                    print(await scraper.job_posting_apply())
                    job_posting_qualifier.status = 'Applied'
                    print(put_record_into_airtable(job_posting_qualifier.convert_to_json()))
                else:
                    print(put_record_into_airtable(job_posting_qualifier.convert_to_json()))
        return job_dict

        
# async def execute_functionality():
#     try:
#         scraper = UpworkScraper()
#         await scraper.login()
#         rss_feed = await scraper.rss_feed_scrape()

#         result = await driver(rss_feed, scraper)  # Call the driver function with the RSS feed data

#         return JsonResponse({'message': 'Functionality executed successfully', 'result': result.data})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)