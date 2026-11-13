from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(100))
    graduation_year = db.Column(db.Integer)
    cgpa = db.Column(db.Numeric(4, 2))
    role = db.Column(db.String(20), nullable=False, default="student")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    applications = db.relationship("Application", back_populates="student", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False, unique=True)
    website = db.Column(db.String(255))
    description = db.Column(db.Text)
    location = db.Column(db.String(160))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    jobs = db.relationship("Job", back_populates="company", cascade="all, delete-orphan")


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(160))
    minimum_cgpa = db.Column(db.Numeric(4, 2), default=0)
    eligible_departments = db.Column(db.String(255), default="All")
    graduation_year = db.Column(db.Integer)
    deadline = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    company = db.relationship("Company", back_populates="jobs")
    applications = db.relationship("Application", back_populates="job", cascade="all, delete-orphan")

    def is_student_eligible(self, student):
        if not student.cgpa or float(student.cgpa) < float(self.minimum_cgpa or 0):
            return False
        departments = (self.eligible_departments or "All").strip().lower()
        if departments not in ("all", ""):
            allowed = [item.strip() for item in departments.split(",")]
            if (student.department or "").strip().lower() not in allowed:
                return False
        if self.graduation_year and student.graduation_year != self.graduation_year:
            return False
        return True


class Application(db.Model):
    __tablename__ = "applications"
    __table_args__ = (db.UniqueConstraint("student_id", "job_id", name="uq_student_job_application"),)

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="Submitted")
    applied_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student = db.relationship("User", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")


class PlacementRecord(db.Model):
    __tablename__ = "placement_records"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    job_title = db.Column(db.String(160), nullable=False)
    package_lpa = db.Column(db.Numeric(8, 2))
    placement_date = db.Column(db.Date)

    student = db.relationship("User")
    company = db.relationship("Company")


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None
