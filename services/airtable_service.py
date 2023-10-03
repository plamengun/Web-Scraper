import requests
from dotenv import load_dotenv
import os 


load_dotenv()

api_key = os.environ.get('AIRTABLE_ACCESS_TOKEN')
base_id = os.environ.get('AIRTABLE_BASE_ID')
table_name = os.environ.get('AIRTABLE_TABLE_NAME')
endpoint = f'https://api.airtable.com/v0/{base_id}/{table_name}'


def put_record_into_airtable(record_data: dict):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    # record_data = {
    #     "fields": {
    #         "time_of_application_attempt": record_data.time_of_application_attempt,
    #         "result_of_application_attempt": record_data.result_of_application_attempt,
    #         "title": record_data.title,
    #         "url": record_data.url,
    #         "posted_before": record_data.posted_before,
    #         "description": record_data.description,
    #         "connects_required": record_data.connects_required,
    #         "connects_available": record_data.connects_available,
    #         "client_country": record_data.client_country,
    #         "gpt_qualifying_answer": record_data.gpt_qualifying_answer
    #     }
    # }

    response = requests.post(endpoint, headers=headers, json=record_data)

    if response.status_code == 200:
        print("Record inserted successfully")
    else:
        print(f"Error: {response.status_code} - {response.text}")


# record_data = {

#     "records": []

# }