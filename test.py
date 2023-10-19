
from dotenv import load_dotenv
from common.variables import APPLY_PROMPT
from pydantic import BaseModel
from typing import List
from common.variables import *
from services.gpt_requests_service import askgpt


load_dotenv()


class Job_Application(BaseModel):
    job_posting_description: str
    question_texts: List[str] | None = None
    _answer_texts: List[str] | None = None
    chat_log: List[str] | None = None

    def add_description_to_questions(self):
        if self.question_texts is None:
            self.question_texts = [self.job_posting_description] 
        self.question_texts.insert(0, self.job_posting_description)

    @property
    def answer_texts(self):
        if self._answer_texts is None:
            self._answer_texts = self.extract_answers_from_log()
        return self._answer_texts
    
    @answer_texts.setter
    def answer_texts(self, value):
        self._answer_texts = value

    def extract_answers_from_log(self) -> List[str]:
        if self.chat_log is None:
            raise ValueError('No answers found')
        answer_texts = [entry['content'] for entry in self.chat_log if entry['role'] == 'assistant']
        return answer_texts 