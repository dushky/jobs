from django.urls import reverse
from rest_framework import status

from api.tests.base import JobAPITestCase


class JobListViewTests(JobAPITestCase):

    def test_list_jobs_success(self):
        url = reverse('job-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
