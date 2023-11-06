from asgiref.sync import sync_to_async
from scrape_runs.models import JobPostingQualifier, ScrapeRun
from scrape_runs.serializers import ScrapeRunSerializer
from users.models import User
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from users.serializers import UserSerializer
import jwt, datetime

#TODO Error handling for all db operations
@sync_to_async
def check_existing_job_posting(title: str) -> bool | None:
    #TODO Wrap in try/except for error handling
    existing_job_posting = JobPostingQualifier.objects.filter(title=title).first()
    if existing_job_posting:
        return True
    return None


@sync_to_async
def save_job_posting_qualifier(job_posting_qualifier: JobPostingQualifier) -> bool | None:
    #TODO Wrap in try/except for error handling
    job_posting_qualifier.save()
    return 'Job Posting processed sucessfully.'


@sync_to_async
def get_logged_in_user(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    user = User.objects.filter(id= payload['id']).first()
    serializer = UserSerializer(user)
    return serializer


@sync_to_async
def create_scrape_run(user_id):
    scrape_run = ScrapeRun.objects.create(user_id=user_id, start_time=datetime.datetime.now())
    serializer = ScrapeRunSerializer(scrape_run)
    return serializer


@sync_to_async
def get_scrape_run_by_id(scrape_run_id):
    scrape_run = ScrapeRun.objects.filter(id=scrape_run_id).first()
    return scrape_run