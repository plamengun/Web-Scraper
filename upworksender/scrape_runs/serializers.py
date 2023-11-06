from rest_framework import serializers
from .models import JobPostingQualifier, ScrapeRun
from asgiref.sync import sync_to_async

class JobPostingQualifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostingQualifier
        fields = [
            'id',
            'title',
            'url',
            'posted_before',
            'description',
            'connects_required',
            'connects_available',
            'client_country',
            'application_page_url',
            'client_properties',
            'gpt_response',
            'gpt_answer',
            'status',
            'scrape_run',
        ]

    def validate_status(self, value):
        if value != 'Applied':
            raise serializers.ValidationError('Invalid job_posting status value')
        return value

    def validate(self, data):
        if 'status' in data:
            self.validate_status(data['status'])
        return data
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance        
    

class ScrapeRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapeRun
        fields = ('id', 'start_time', 'finish_time')

    @sync_to_async
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance





# {
#     "title": "asd",
#     "url": "asd",
#     "posted_before": "asd",
#     "description": "asd",
#     "connects_required": "asd",
#     "connects_available": "asd",
#     "client_country": "asd",
#     "application_page_url": "asd",
#     "client_properties": "asd",
#     "gpt_response": "asd",
#     "gpt_answer": "asd",
#     "status": "Not Applied",
#     "scrape_run": "asd"
# }