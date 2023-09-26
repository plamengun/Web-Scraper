import requests
from dotenv import load_dotenv
import os 


load_dotenv()

api_key = os.environ.get('AIRTABLE_ACCESS_TOKEN')
base_id = os.environ.get('AIRTABLE_BASE_ID')
table_name = os.environ.get('AIRTABLE_TABLE_NAME')


endpoint = f'https://api.airtable.com/v0/{base_id}/{table_name}'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

record_data = {
    'fields': {
        'title': 'test',
        'url': 'test',
        'posted_on': 'test',
        'description': 'test',
        'connects_required': 12,
        'connects_available': 13,
        'client_country': 'asd',
        'chat_gpt_outputs': '',
    }
}

response = requests.post(endpoint, headers=headers, json=record_data)

if response.status_code == 200:
    print("Record inserted successfully")
else:
    print(f"Error: {response.status_code} - {response.text}")




record_data = {

    "records": []

}