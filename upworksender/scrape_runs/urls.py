from django.urls import path
from .views import ScraperRunView

urlpatterns = [
    path('scraper', ScraperRunView.as_view()),
]