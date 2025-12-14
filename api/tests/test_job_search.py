from django.urls import reverse
from rest_framework import status

from api.tests.base import JobAPITestCase


class JobSearchFilterTests(JobAPITestCase):

    def setUp(self):
        self.url = reverse('job-list')

    def test_search_and_filter_success(self):
        response = self.client.get(self.url, {'q': 'Python', 'country': 'USA'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)
        
        for job in response.data:
            self.assertEqual(job['country'], 'USA')

        # Assert relevance of search results
        ids = [job['id'] for job in response.data]
        
        index_job1 = ids.index('1')
        index_job3 = ids.index('3')
        
        self.assertLess(index_job1, index_job3, "Job with title match should rank higher than description match")

    def test_search_returns_zero_results(self):
        response = self.client.get(self.url, {'q': 'NonExistentTechnology12345'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
