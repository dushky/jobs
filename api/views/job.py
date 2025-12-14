from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from api.filters import JobFilter
from api.models import Job
from api.serializers.job import JobListSerializer, JobDetailSerializer


class JobPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class JobListView(generics.ListAPIView):
    queryset = Job.objects.select_related('organization', 'country').prefetch_related('skills')
    serializer_class = JobListSerializer
    # pagination_class = JobPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = JobFilter


class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.select_related('organization', 'country').prefetch_related('skills')
    serializer_class = JobDetailSerializer
    lookup_field = 'id'
