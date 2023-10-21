from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import ScrapeRun
from .serializers import ScrapeRunSerializer, JobPostingQualifierSerializer
from logic.driver import execute_functionality


class ScraperRunView(APIView):
    queryset = ScrapeRun.objects.all()
    seralizer = ScrapeRunSerializer

    def post(self, request):
        response = execute_functionality()
        return response


class JobPostingQualifierView(APIView):
    def post(self, request):
        serializer = JobPostingQualifierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)