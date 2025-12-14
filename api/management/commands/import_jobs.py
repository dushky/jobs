import json
import os
import time
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.models import Job, Organization, Country, Skill


DEFAULT_JSON_FILE = 'be-jobs-data-example.json'


class Command(BaseCommand):
    help = 'Import jobs from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            nargs='?',
            default=os.path.join(settings.BASE_DIR, DEFAULT_JSON_FILE),
            help=f'Path to the JSON file to import (default: {DEFAULT_JSON_FILE})'
        )

    def handle(self, *args, **options):
        json_file_path = options['json_file']

        if not os.path.exists(json_file_path):
            raise CommandError(f'File "{json_file_path}" does not exist')

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            raise CommandError(f'File "{json_file_path}" is not a valid JSON file')

        if not isinstance(data, list):
            raise CommandError('JSON file must contain a list of job objects')

        self.stdout.write(f'Starting import of {len(data)} jobs...')
        start_time = time.time()

        imported_count, skipped_count = self._import_jobs(data)

        duration = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(
            f'Import finished. Imported: {imported_count}, Skipped: {skipped_count}, '
            f'Duration: {duration:.2f}s'
        ))

    def _import_jobs(self, data):
        imported_count = 0
        skipped_count = 0

        with transaction.atomic():
            for job_data in data:
                job_id = job_data.get('id')
                if not job_id:
                    continue

                if Job.objects.filter(id=job_id).exists():
                    skipped_count += 1
                    continue

                self._create_job(job_id, job_data)
                imported_count += 1

        return imported_count, skipped_count

    def _create_job(self, job_id, job_data):
        organization = self._get_or_create_organization(job_data.get('organization'))
        country = self._get_or_create_country(job_data.get('country'))

        job = Job.objects.create(
            id=job_id,
            title=job_data.get('title', ''),
            description=job_data.get('description', ''),
            organization=organization,
            country=country,
        )

        skills = self._get_or_create_skills(job_data.get('skills', []))
        if skills:
            job.skills.set(skills)

        return job

    def _get_or_create_organization(self, name):
        if not name:
            return None
        name = name.strip()
        org, _ = Organization.objects.get_or_create(
            name__iexact=name,
            defaults={'name': name}
        )
        return org

    def _get_or_create_country(self, name):
        if not name:
            return None
        name = name.strip()
        country, _ = Country.objects.get_or_create(
            name__iexact=name,
            defaults={'name': name}
        )
        return country

    def _get_or_create_skills(self, skill_names):
        skills = []
        for name in skill_names:
            name = name.strip()
            if name:
                skill, _ = Skill.objects.get_or_create(
                    name__iexact=name,
                    defaults={'name': name}
                )
                skills.append(skill)
        return skills
