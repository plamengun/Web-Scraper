from django.urls import path
from .views import ScrapeRunView, JobPostingQualifierView

urlpatterns = [
    path('scraper', ScrapeRunView.as_view()),
    path('job_posting', JobPostingQualifierView.as_view(),)
]