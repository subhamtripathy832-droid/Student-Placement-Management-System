# Database Design

The application uses a relational MySQL database. SQLAlchemy model definitions are in `models.py`; the corresponding reference DDL is in `database/schema.sql`.

## Tables and relationships

| Table | Purpose | Main relationship |
|---|---|---|
| `students` | Student and admin accounts; student academic profile | One student can have many applications |
| `companies` | Company details | One company can have many jobs and placement records |
| `jobs` | Job descriptions and eligibility criteria | One job can receive many applications |
| `applications` | Student applications and statuses | Each application belongs to one student and one job |
| `placement_records` | Final placement details | Each record links one student and one company |

## Relationship summary

- `companies.id` → `jobs.company_id` (one-to-many)
- `students.id` → `applications.student_id` (one-to-many)
- `jobs.id` → `applications.job_id` (one-to-many)
- `students.id` → `placement_records.student_id` (one-to-many)
- `companies.id` → `placement_records.company_id` (one-to-many)

## Important constraints

- Student email is unique.
- Company name is unique in this starter version.
- A student can apply to a particular job only once (`student_id`, `job_id` unique pair).
- Foreign keys connect applications and jobs to their parent records.

## Notes

The `students` table stores both student and administrator accounts. The `role` field distinguishes `student` from `admin`; administrator accounts should only be created using the `create_admin.py` script, not through the public registration page.
