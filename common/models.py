from playwright.sync_api import JSHandle


class Job_Posting():
    def __init__(self, 
                 title: str | None, 
                 url: str | None, 
                 posted_before: str | None, 
                 description: str | None,
                 connects_required: int | None,
                 connects_available: int | None,
                 client_country: str | None,
                 application_page_url: str | None) -> None:
        self._title = title
        self._url = url
        self._posted_before = posted_before
        self._description = description
        self._connects_required = connects_required
        self.connects_available = connects_available
        self._client_country = client_country
        self._application_page_url = application_page_url

    @property
    def title(self):
        return self._title
    
    @property
    def url(self):
        return self._url
    
    @property
    def posted_before(self):
        return self._posted_before
    
    @property
    def description(self):
        return self._description
    
    @property
    def connects_required(self):
        return self._connects_required
    
    @property
    def client_country(self):
        return self._client_country
    
    @property
    def application_page_url(self):
        return self._application_page_url
    
    def check_available_connects(self) -> str | None:
        if self.connects_available - self.connects_required >= 0:
            return True
        return False

    def convert_to_json(self):
        job_post_json = {
            "fields": {
                "title": self.title,
                "url": self.url,
                "posted_before": self.posted_before,
                "description": self.description,
                "connects_required": self.connects_required,
                "connects_available": self.connects_available,
                "client_country": self.client_country,
            }
        }
        return job_post_json


class Job_Application():
    def __init__(self,
                 job_posting_description: str,
                 cover_letter_field: JSHandle,
                 question_fields: list[JSHandle] | None = None,
                 question_texts: list[str] | None = None,
                 chat_log: list[str] | None = None) -> None:
        self.job_posting_description = job_posting_description
        self.cover_letter_field = cover_letter_field
        self.question_fields = question_fields
        self.question_texts= question_texts
        self.chat_log = chat_log

    def add_description_to_questions(self):
        if self.question_texts is None:
            self.question_texts = [self.job_posting_description] 
        self.question_texts.insert(0, self.job_posting_description)

    def extract_answers_from_log(self) -> list[str]:
        answer_texts = [entry['content'] for entry in self.chat_log if entry['role'] == 'assistant']
        return answer_texts



    #ToDo Automatically add job_posting_description in 0 position in answer_texts upon instantiation





# class Job_Posting_Record(Job_Posting):
#     def __init__(self, 
#                  job_link, 
#                  date_submitted, 
#                  time_job_posted_ago, 
#                  job_total_proposals, 
#                  sent_status,
#                  connects_spent, 
#                  boosted,
#                  boosted_place,
#                  uk_only) -> None:
#         self.job_link = job_link
#         self.date_submitted = date_submitted
#         self.time_job_posted_ago = time_job_posted_ago
#         self.job_total_proposals = job_total_proposals
#         self.sent_status = sent_status
#         self.connects_spent = connects_spent
#         self.boosted = boosted
#         self.boosted_place = boosted_place
#         self.uk_only = uk_only

