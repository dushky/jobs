from django.db import models
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex
from django.db.models import Value


class Job(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    country = models.ForeignKey(
        'Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    skills = models.ManyToManyField('Skill', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        ordering = ['-id']
        indexes = [
            GinIndex(fields=['search_vector']),
        ]

    def __str__(self):
        return self.title

    def update_search_vector(self):
        skills_text = ' '.join(self.skills.values_list('name', flat=True))
        Job.objects.filter(pk=self.pk).update(
            search_vector=(
                SearchVector('title', weight='A', config='simple') +
                SearchVector('description', weight='B', config='simple') +
                SearchVector(Value(skills_text), weight='B', config='simple')
            )
        )
