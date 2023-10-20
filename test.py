
from dotenv import load_dotenv
from common.variables import APPLY_PROMPT
from pydantic import BaseModel
from typing import List
from common.variables import *
from services.gpt_requests_service import askgpt


load_dotenv()


# insert into scrape_runs_scraperun(id, start_time, finish_time, user_id)
# values(1, '2023-10-11 13:34', '2023-10-11 13:34', 1);

# select * from scrape_runs_scraperun;
# select * from scrape_runs_jobpostingqualifier;