from django.urls import path

from api.views.job import JobListView, JobDetailView

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/<str:id>/', JobDetailView.as_view(), name='job-detail'),
]

