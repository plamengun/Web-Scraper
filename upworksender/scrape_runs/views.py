from adrf.views import APIView as AsyncAPIView
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response
from .models import ScrapeRun
from .serializers import ScrapeRunSerializer, JobPostingQualifierSerializer
from logic.driver import driver
from logic.services.scraper import UpworkScraper


# class ScraperRunView(APIView):
#     queryset = ScrapeRun.objects.all()
#     seralizer = ScrapeRunSerializer

#     async def post(self, request):
#         response = await execute_functionality()
#         return response

class ScraperRunView(AsyncAPIView):
    queryset = ScrapeRun.objects.all()
    serializer_class = ScrapeRunSerializer

    async def post(self, request):
        try:
            scraper = UpworkScraper()
            await scraper.login()
            rss_feed = await scraper.rss_feed_scrape()

            result = await driver(rss_feed, scraper)  # Call the driver function with the RSS feed data

            return Response({'message': 'Functionality executed successfully', 'result': result.data})
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class JobPostingQualifierView(APIView):
    def post(self, request):
        serializer = JobPostingQualifierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)