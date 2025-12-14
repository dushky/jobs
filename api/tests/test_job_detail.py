from django.urls import reverse
from rest_framework import status

from api.tests.base import JobAPITestCase


class JobDetailViewTests(JobAPITestCase):

    def test_get_job_detail_success(self):
        url = reverse('job-detail', kwargs={'id': '1'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], '1')
        self.assertIn('description', response.data)

    def test_job_detail_returns_404(self):
        url = reverse('job-detail', kwargs={'id': 'nonexistent-job-id'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
