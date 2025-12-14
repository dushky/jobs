from django.urls import path

from api.views.job import JobListView

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job-list'),
]

