
class Job_Posting():
    def __init__(self, 
                 title: str | None, 
                 url: str | None, 
                 posted_before: str | None, 
                 description: str | None,
                 connects_required: int | None,
                 connects_available: int | None,
                 client_country: str | None,
                 chat_gpt_outputs: dict | None = None) -> None:
        self._title = title
        self._url = url,
        self._posted_before = posted_before
        self._description = description
        self._connects_required = connects_required
        self.connects_available = connects_available
        self._client_country = client_country
        self.chat_gpt_outputs = chat_gpt_outputs

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
    
    def check_available_connects(self) -> str | None:
        if self.connects_available - self.connects_required >= 0:
            return 'True'

    def check_for_gpt_response(self):
        if self.chat_gpt_outputs:
            return 'True'

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
                "chat_gpt_outputs": self.chat_gpt_outputs,
            }
        }
        return job_post_json



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

