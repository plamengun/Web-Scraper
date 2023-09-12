from playwright.sync_api import sync_playwright, JSHandle
from typing import List
from dotenv import load_dotenv
import os
import re

load_dotenv()

# def pw_job_posting():
# print(pw_job_posting_scrape())


def calculate_connects(connects_required: int = 12, available_connects: int = 1) -> str | None:
    if available_connects - connects_required >= 0:
        return 'True'




    

    


def pw_proposal_submit(cover_letter_field, questions_with_fields_dict):
    pass