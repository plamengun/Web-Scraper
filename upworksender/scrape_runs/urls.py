from django.urls import path
from .views import ScraperRunView, JobPostingQualifierView

urlpatterns = [
    path('scraper', ScraperRunView.as_view()),
    path('job_posting', JobPostingQualifierView.as_view(),)
]