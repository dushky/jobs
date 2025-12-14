# Jobs API Project

A Django-based REST API for listing and searching job advertisements.

**Python Version:** 3.12

## Setup & Running

1. **Create & Activate Virtual Environment**
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Import Data** (using default file `be-jobs-data-example.json`)
   ```bash
   python manage.py import_jobs
   ```

4. **Run Server**
   ```bash
   python manage.py runserver
   ```

## API Usage

### 1. List Jobs
**Endpoint:** `GET /api/v1/jobs/`

Supports full-text search, filtering, and pagination.

**Parameters:**
- `q`: Search query (searches title, description, skills). Title matches have higher relevance.
- `country`: Filter by exact country name.
- `page`: Page number (default: 1).
- `page_size`: Results per page (default: 10, max: 100).

**Examples:**

| Example | URL                                                                                                                                          |
|---------|----------------------------------------------------------------------------------------------------------------------------------------------|
| List all jobs | [http://localhost:8000/api/v1/jobs/](http://localhost:8000/api/v1/jobs/)                                                                     |
| Search for "python" | [http://localhost:8000/api/v1/jobs/?q=python](http://localhost:8000/api/v1/jobs/?q=python)                                                   |
| Search for "software engineer" | [http://localhost:8000/api/v1/jobs/?q=software+engineer](http://localhost:8000/api/v1/jobs/?q=software+engineer)                             |
| Filter by country | [http://localhost:8000/api/v1/jobs/?country=Taiwan](http://localhost:8000/api/v1/jobs/?country=Taiwan)                                       |
| Search + country filter | [http://localhost:8000/api/v1/jobs/?q=developer&country=United+States](http://localhost:8000/api/v1/jobs/?q=developer&country=United+States) |

### 2. Job Detail
**Endpoint:** `GET /api/v1/jobs/{id}/`

Returns full job details including description.

| Example | URL |
|---------|-----|
| Get job | [http://localhost:8000/api/v1/jobs/1677637499/](http://localhost:8000/api/v1/jobs/1677637499/) |
## Future Improvements
**Salary** - Add salary field to the Job model and allow filtering by salary range to find jobs that meet compensation expectations.
**User Profile** - Implement user profiles linked to skills, organizations and countries allowing applicants filter for compatible jobs based on their saved preferences.

## Time Tracking

- **1h** - Bootstrapping project & DB models (Initial setup, defining Job/Country/Skill models)
- **1.5h** - Data Import Script
- **1h** - API Implementation (Views, Serializers, Pagination, Filtering, Ordering)
- **0.5h** - Testing (Unit tests for APIs, edge cases, relevance ordering)

**Total:** ~4 hours
