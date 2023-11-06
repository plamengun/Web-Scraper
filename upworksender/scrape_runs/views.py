from adrf.views import APIView as AsyncAPIView
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response
from .serializers import JobPostingQualifierSerializer
from logic.driver import driver
from logic.common.database import get_logged_in_user, create_scrape_run
from logic.services.scraper import UpworkScraper



class ScrapeRunView(AsyncAPIView):
    async def post(self, request):
        user_serializer = await get_logged_in_user(request=request)
        user_id = user_serializer.data["id"]
        scrape_run_serializer = await create_scrape_run(user_id)
        scrape_run_id = scrape_run_serializer.data["id"]
        try:
            scraper = UpworkScraper()
            await scraper.login()
            rss_feed = await scraper.rss_feed_scrape()
            result = await driver(rss_feed, scraper, scrape_run_id)  # Call the driver function with the RSS feed data
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