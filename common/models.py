
class Job_Posting():
    def __init__(self, 
                 title: str | None, 
                 url: str | None, 
                 posted_before: str | None, 
                 description: str | None,
                 connects_required: int | None,
                 connects_available: int | None,
                 client_country: str | None,
                 application_page_url: str | None,
                 eligible_to_apply: bool | None=None) -> None:
        self._title = title
        self._url = url
        self._posted_before = posted_before
        self._description = description
        self._connects_required = connects_required
        self.connects_available = connects_available
        self._client_country = client_country
        self._application_page_url = application_page_url
        self.eligible_to_apply = eligible_to_apply

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
                 question_texts: list[str] | None = None,
                 answer_texts: list[str] | None = None,
                 chat_log: list[str] | None = None) -> None:
        self.job_posting_description = job_posting_description
        self.question_texts= question_texts
        self._answer_texts = answer_texts
        self.chat_log = chat_log

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

    def extract_answers_from_log(self) -> list[str]:
        if self.chat_log is None:
            raise ValueError('No answers found')
        answer_texts = [entry['content'] for entry in self.chat_log if entry['role'] == 'assistant']
        return answer_texts 


class Job_Posting_Qualifier(Job_Posting):
    def __init__(self,
                 title: str | None, 
                 url: str | None, 
                 posted_before: str | None,
                 description: str | None, 
                 connects_required: int | None, 
                 client_properties: str | None):
        super().__init__(title, url, posted_before, description, connects_required, None, None, None)
        self._client_properties = client_properties

    @property
    def client_properties(self):
        return self._client_properties

    def convert_to_str(self):
        job_post_qualifier_str += f"{self.client_properties}\n"
        job_post_qualifier_str = f"Title: {self.title}\n"
        job_post_qualifier_str += f"Posted Before: {self.posted_before}\n"
        job_post_qualifier_str += f"Description: {self.description}\n"
        job_post_qualifier_str += f"Connects Required: {self.connects_required}\n"
        return job_post_qualifier_str