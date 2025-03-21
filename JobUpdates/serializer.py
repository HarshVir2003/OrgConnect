from rest_framework import serializers
from JobUpdates.models import JobUpdates


class JobUpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobUpdates
        fields = ['title', 'company_name', 'location', 'job_url', 'description', 'posted_at']

    def validate(self, data):
        return data
