from rest_framework import serializers

from api.models import Job


class JobListSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()
    country = serializers.StringRelatedField()
    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'organization', 'country', 'skills', 'date_created']


class JobDetailSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()
    country = serializers.StringRelatedField()
    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'organization', 'country', 'skills', 'date_created']

