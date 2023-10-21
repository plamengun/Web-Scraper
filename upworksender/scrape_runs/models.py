from django.db import models
import datetime
from pydantic import BaseModel
from typing import List


class ScrapeRun(models.Model):
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    
    def get_job_posting_qualifiers(self):
        return JobPostingQualifier.objects.filter(scrape_run=self)


class JobPostingQualifier(models.Model):
    title = models.CharField(max_length=400)
    url = models.URLField()
    posted_before = models.TextField()
    description = models.TextField()
    connects_required = models.PositiveIntegerField()
    connects_available = models.PositiveIntegerField()
    client_country = models.CharField(max_length=100)
    application_page_url = models.URLField()
    client_properties = models.TextField()
    gpt_response = models.TextField(blank=True, null=True)
    gpt_answer = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Not Applied')
    scrape_run = models.ForeignKey(ScrapeRun, on_delete=models.CASCADE)


    def change_status(self):
        if self.status != 'Not Applied':
            return 'Status already set to Applied'
        self.status = 'Applied'
        return 'Status set to Applied'

    def check_available_connects(self) -> bool:
        if self.connects_available - self.connects_required >= 0:
            return True
        return False

    def parse_gpt_response(self):
        if self.gpt_response is None:
            raise ValueError('No qualification response str provided from ChatGPT.')
        response_texts = [entry['content'] for entry in self.gpt_response if entry['role'] == 'assistant']
        return response_texts
    
    def check_gpt_answer(self):
        if self.gpt_answer is None:
            raise ValueError('No qualification answer str provided from ChatGPT.')
        answer_texts_list = self._parse_gpt_answer()
        if 'YES' in answer_texts_list[0]:
            self.gpt_answer = answer_texts_list[1]
            return True
        elif 'NO' in answer_texts_list[0]:
            self.gpt_answer = answer_texts_list[1]
            return False
        self.gpt_answer='Gpt Qualification Answer not found.'
        return False
    
    def _parse_gpt_answer(self):
        if self.gpt_answer is None:
            raise ValueError('No qualification answer str provided from ChatGPT.')
        answer_texts = self.gpt_answer[0].strip()
        answer_texts_list = answer_texts.split('\n')
        final_answer_texts_list = [el for el in answer_texts_list if 'Answer' in el or 'Explanation' in el]
        return final_answer_texts_list
        
    def _get_current_datetime_as_string(self):
        current_datetime = datetime.datetime.now()
        return current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    def convert_to_str(self):
        job_post_qualifier_str = f"Title: {self.title}\n"
        job_post_qualifier_str += f"Posted Before: {self.posted_before}\n"
        job_post_qualifier_str += f"Connects Required: {self.connects_required}\n"
        job_post_qualifier_str += f"{self.client_properties}\n"
        job_post_qualifier_str += f"Job Post Description: {self.description}"
        job_post_qualifier_str += f"{self.client_properties}"
        return job_post_qualifier_str
    
    def convert_to_json(self):
        job_post_json = {
            "fields": {
                "time_of_application_attempt": self._get_current_datetime_as_string(),
                "result_of_application_attempt": self.status,
                "title": self.title,
                "url": self.url,
                "posted_before": self.posted_before,
                "description": self.description,
                "connects_required": self.connects_required,
                "connects_available": self.connects_available,
                "client_country": self.client_country,
                "gpt_qualifying_answer": self.gpt_answer
            }
        }
        return job_post_json
    

class JobApplication(BaseModel):
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
    