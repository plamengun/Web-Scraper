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
    #TODO Error: 422 - {"error":{"type":"INVALID_VALUE_FOR_COLUMN","message":"Field \"title\" cannot accept the provided value"}}
    response = requests.post(endpoint, headers=headers, json=record_data)

    if response.status_code == 200:
        return "Record inserted successfully"
    else:
        return f"Error: {response.status_code} - {response.text}"
