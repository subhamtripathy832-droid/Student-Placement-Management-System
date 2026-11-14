# Student Placement Management System

A starter full-stack college placement portal built with **Python, Flask, MySQL, HTML, CSS and JavaScript**. It provides separate student and administrator workflows for managing job opportunities and placement applications.

> **Project status:** This repository is a functional starter/MVP scaffold, not a finished production deployment. Authentication, student profile editing, job browsing/application submission, company management and basic application-status management are included. Features such as resume upload, email notifications, advanced analytics, placement-record entry screens, automated test coverage and deployment hardening are future enhancements.

## Features

### Student
- Register and log in with a password hash (not a plain-text password).
- Maintain basic profile information: department, graduation year and CGPA.
- Browse active job postings and see the stated eligibility criteria.
- Apply to an eligible job once and track the application status.

### Administrator
- Separate administrator role and protected dashboard.
- View student, company, job, application and placement counts.
- Add company records and create job postings.
- View applications and update their status.

### Data model
- `students` — student/admin accounts and academic profile fields.
- `companies` — company details.
- `jobs` — vacancies and eligibility criteria.
- `applications` — student applications and current status.
- `placement_records` — final placement details.

## Technology stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript, Jinja templates |
| Backend | Python 3, Flask |
| ORM / database access | Flask-SQLAlchemy |
| Database | MySQL 8+ (PyMySQL driver) |
| Authentication | Flask-Login, Werkzeug password hashing |
| Form protection | Flask-WTF CSRF protection |

## Repository structure

```text
Student-Placement-Management-System/
├── app.py
├── app/
│   └── __init__.py
├── config.py
├── extensions.py
├── models.py
├── routes/
│   ├── auth.py
│   ├── student.py
│   ├── admin.py
│   └── company.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── admin_dashboard.html
│   ├── jobs.html
│   ├── profile.html
│   ├── applications.html
│   ├── companies.html
│   ├── company_directory.html
│   ├── students.html
│   ├── new_job.html
│   └── errors/
├── static/css/style.css
├── static/js/script.js
├── database/schema.sql
├── docs/
├── screenshots/
├── init_db.py
├── create_admin.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Prerequisites

- Python 3.10 or newer
- MySQL Server 8.0 or newer
- Git (for GitHub upload)
- A terminal / VS Code

## Run locally

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR-USERNAME/Student-Placement-Management-System.git
   cd Student-Placement-Management-System
   ```

2. **Create and activate a virtual environment**

   Windows PowerShell:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   macOS / Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create the MySQL database**

   In MySQL, run:

   ```sql
   CREATE DATABASE placement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

   You may also review `database/schema.sql`. The application creates its tables from the SQLAlchemy models in the next step.

5. **Configure environment variables**

   Copy `.env.example` to `.env`. Update `SECRET_KEY` and `DATABASE_URL` with your own values. Example:

   ```env
   SECRET_KEY=your-long-random-secret
   DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/placement_db?charset=utf8mb4
   ADMIN_NAME=Placement Administrator
   ADMIN_EMAIL=admin@example.com
   ADMIN_PASSWORD=use-a-long-unique-password
   ```

   Do not commit `.env` to GitHub. It is ignored by `.gitignore`.

6. **Create database tables and an administrator**

   ```bash
   python init_db.py
   python create_admin.py
   ```

   The administrator credentials come from the `ADMIN_*` values in `.env`. The script refuses passwords shorter than 12 characters.

7. **Start the development server**

   ```bash
   python app.py
   ```

   Open `http://127.0.0.1:5000` in your browser.

## Basic workflow

1. Register a student account and complete the academic profile.
2. Log in as the administrator using the account created by `create_admin.py`.
3. Add one or more companies from the Companies page.
4. Create a job posting and define its minimum CGPA, eligible departments and graduation year.
5. Log in as a student, browse jobs and apply when eligible.
6. As administrator, open Applications and update the application status.

## Eligibility rules in this starter

- The student's CGPA must be present and meet or exceed the job's minimum CGPA.
- Department must match one of the comma-separated eligible department values, unless the job is set to `All`.
- If a graduation year is specified for a job, it must match the student's graduation year.

These are sample rules. Confirm your institution's actual placement policy before using them for real decisions. The eligibility check is not a substitute for final verification by a placement officer.

## Important security notes

- Never publish real passwords, database credentials, `.env`, student personal data or real placement records in the repository.
- The included development server uses `debug=True`; do not use it for public deployment.
- Set a strong, random `SECRET_KEY` and use a restricted MySQL database account.
- Before production use, configure HTTPS, secure cookie settings, backups, logging, rate limiting, stronger input validation, privacy controls and a production WSGI server.
- Review authorization rules and test the application thoroughly before storing real student information.

## Documentation

- [Project overview](docs/project_overview.md)
- [Database design](docs/database_design.md)
- [Installation guide](docs/installation_guide.md)
- [User guide](docs/user_guide.md)
- [Development roadmap](docs/roadmap.md)

## Screenshots

## Application Screenshots

### 1. Admin Dashboard
The administrator dashboard provides an overview of students, companies, job postings and placement applications.

![Admin Dashboard](screenshots/admin-dashboard.png)

### 2. Company Management
Administrators can add companies and manage company information.

![Company Management](screenshots/company-management.png)

### 3. Job Listings
Students can browse available job opportunities and view eligibility requirements.

![Job Listings](screenshots/job-listings.png)

### 4. Student Dashboard
The student dashboard provides access to profile information, available jobs and application details.

![Student Dashboard](screenshots/student-dashboard.png)

### 5. My Applications
Students can view their submitted applications and track their current status.

![My Applications](screenshots/my-applications.png)

### 6. Admin Application Management
Administrators can review applications and update their status.

![Admin Applications](screenshots/admin-applications.png)

## Future enhancements

- Resume upload and profile document management.
- Email notifications for application status changes.
- Search, filters and pagination for jobs and students.
- CSV/Excel reports for placement coordinators.
- Placement-record creation and editing interface.
- Audit logs and more granular permissions.
- Automated tests and production deployment configuration.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
