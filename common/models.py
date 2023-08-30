
class Job_Posting():
    def __init__(self, 
                 title: str | None, 
                 url: str | None, 
                 posted_on: str | None, 
                 description: str | None,
                 connects_required: int | None,
                 connects_available: int | None,
                 client_country: str | None,
                 chat_gpt_outputs: dict | None) -> None:
        self._title = title
        self._url = url,
        self._posted_on = posted_on
        self._description = description
        self._connects_required = connects_required
        self._connects_available = connects_available
        self._client_country = client_country
        self._chat_gpt_outputs = chat_gpt_outputs

    @property
    def title(self):
        return self._title
    
    @property
    def url(self):
        return self._url
    
    @property
    def posted_on(self):
        return self._posted_on
    
    @property
    def description(self):
        return self._description
    
    @property
    def connects_required(self):
        return self._connects_required
    
    @property
    def connects_available(self):
        return self._connects_available
    
    @property
    def client_country(self):
        return self._client_country
    
    @property
    def chat_gpt_outputs(self):
        return self._chat_gpt_outputs
    

    def check_available_connects(self) -> str | None:
        if self.connects_available - self.connects_required >= 0:
            return 'True'

    def check_for_gpt_response(self):
        if self.chat_gpt_outputs:
            return 'True'




class Job_Posting_Record(Job_Posting):
    def __init__(self, 
                 job_link, 
                 date_submitted, 
                 time_job_posted_ago, 
                 job_total_proposals, 
                 sent_status,
                 connects_spent, 
                 boosted,
                 boosted_place,
                 uk_only) -> None:
        self.job_link = job_link
        self.date_submitted = date_submitted
        self.time_job_posted_ago = time_job_posted_ago
        self.job_total_proposals = job_total_proposals
        self.sent_status = sent_status
        self.connects_spent = connects_spent
        self.boosted = boosted
        self.boosted_place = boosted_place
        self.uk_only = uk_only

