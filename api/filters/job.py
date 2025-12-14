from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F
from django_filters import rest_framework as filters

from api.models import Job


class JobFilter(filters.FilterSet):
    q = filters.CharFilter(method='filter_search')
    country = filters.CharFilter(field_name='country__name', lookup_expr='exact')

    class Meta:
        model = Job
        fields = ['q', 'country']

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset

        query = SearchQuery(value.strip())
        return queryset.filter(search_vector=query).annotate(
            rank=SearchRank(F('search_vector'), query)
        )

    @property
    def qs(self):
        queryset = super().qs

        if self.data.get('q', '').strip():
            return queryset.order_by('-rank', '-id')

        return queryset.order_by('-id')
