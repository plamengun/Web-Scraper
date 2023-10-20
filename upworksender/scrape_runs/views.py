from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import ScrapeRun, JobPostingQualifier
from .serializers import ScrapeRunSerializer, JobPostingQualifierSerializer




class ScraperRunView(APIView):
    queryset = ScrapeRun.objects.all()
    seralizer = ScrapeRunSerializer


class JobPostingQualifierView(APIView):
    def post(self, request):
        serializer = JobPostingQualifierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# def execute_functionality():
#     try:
#         scraper = UpworkScraper()
#         scraper.login()
#         rss_feed = scraper.rss_feed_scrape()

#         # result = driver(rss_feed)  # Call the driver function with the RSS feed data

#         return JsonResponse({'message': 'Functionality executed successfully', 'result': rss_feed})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)
    

# print(execute_functionality())