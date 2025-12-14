from rest_framework.test import APITestCase

from api.models import Job, Organization, Country, Skill


class JobAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls._create_countries()
        cls._create_organizations()
        cls._create_skills()
        cls._create_jobs()

    @classmethod
    def _create_countries(cls):
        cls.country_usa = Country.objects.create(name='USA')
        cls.country_uk = Country.objects.create(name='UK')

    @classmethod
    def _create_organizations(cls):
        cls.org_tech = Organization.objects.create(name='Tech Corp')
        cls.org_startup = Organization.objects.create(name='Startup Inc')

    @classmethod
    def _create_skills(cls):
        cls.skill_python = Skill.objects.create(name='Python')
        cls.skill_django = Skill.objects.create(name='Django')
        cls.skill_javascript = Skill.objects.create(name='JavaScript')

    @classmethod
    def _create_jobs(cls):
        cls.job1 = cls._create_job(
            id='1',
            title='Senior Python Developer',
            description='We are looking for an experienced Python developer.',
            organization=cls.org_tech,
            country=cls.country_usa,
            skills=[cls.skill_python, cls.skill_django],
        )

        cls.job2 = cls._create_job(
            id='2',
            title='Frontend Engineer',
            description='Join our team as a frontend engineer working with React.',
            organization=cls.org_startup,
            country=cls.country_uk,
            skills=[cls.skill_javascript],
        )

        cls.job3 = cls._create_job(
            id='3',
            title='Full Stack Developer',
            description='Python and JavaScript skills required for this role.',
            organization=cls.org_tech,
            country=cls.country_usa,
            skills=[cls.skill_python, cls.skill_javascript],
        )

    @classmethod
    def _create_job(cls, id, title, description, organization, country, skills):
        job = Job.objects.create(
            id=id,
            title=title,
            description=description,
            organization=organization,
            country=country,
        )
        job.skills.add(*skills)
        job.update_search_vector()
        return job
