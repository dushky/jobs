from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from api.models.job import Job
from api.models.skill import Skill


@receiver(post_save, sender=Job)
def update_job_search_vector(sender, instance, created, **kwargs):
    """Update search_vector when Job is saved."""
    if kwargs.get('update_fields') and 'search_vector' in kwargs['update_fields']:
        return
    instance.update_search_vector()


@receiver(m2m_changed, sender=Job.skills.through)
def update_job_search_vector_m2m(sender, instance, action, **kwargs):
    """Update search_vector when skills are added/removed."""
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.update_search_vector()


@receiver(post_save, sender=Skill)
def update_jobs_on_skill_change(sender, instance, created, **kwargs):
    """Update search vectors for all jobs when a skill is renamed."""
    if created:
        return
    for job in instance.job_set.all():
        job.update_search_vector()
