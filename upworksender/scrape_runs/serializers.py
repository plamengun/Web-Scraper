from rest_framework import serializers
from .models import JobPostingQualifier

class JobPostingQualifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostingQualifier
        fields = (
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
        )

    def validate_status(self, value):
        if value != 'Applied':
            raise serializers.ValidationError('Invalid job_posting status value')
        return value

    def validate(self, data):
        if 'status' in data:
            self.validate_status(data['status'])
        return data