from django.urls import reverse
from rest_framework import status

from api.tests.base import JobAPITestCase


class JobSearchFilterTests(JobAPITestCase):

    def setUp(self):
        self.url = reverse('job-list')

    def test_search_and_filter_success(self):
        response = self.client.get(self.url, {'q': 'Python', 'country': 'USA'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertGreaterEqual(len(results), 2)
        
        # Verify country filter works for all results
        for job in results:
            self.assertEqual(job['country'], 'USA')

        # Assert relevance of search results
        ids = [job['id'] for job in results]
        
        index_job1 = ids.index('1')
        index_job3 = ids.index('3')
        
        self.assertLess(index_job1, index_job3, "Job with title match should rank higher than description match")

    def test_search_returns_zero_results(self):
        response = self.client.get(self.url, {'q': 'NonExistentTechnology12345'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 0)
