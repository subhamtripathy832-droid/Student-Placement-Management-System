from datetime import date
from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import Job, Application


student_bp = Blueprint("student", __name__)


def student_only():
    if current_user.role != "student":
        abort(403)


@student_bp.route("/student/dashboard")
@login_required
def dashboard():
    student_only()
    applications = Application.query.filter_by(student_id=current_user.id).order_by(Application.applied_at.desc()).limit(5).all()
    open_jobs = Job.query.filter_by(is_active=True).count()
    return render_template("student_dashboard.html", applications=applications, open_jobs=open_jobs)


@student_bp.route("/jobs")
@login_required
def jobs():
    student_only()
    jobs_list = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
    return render_template("jobs.html", jobs=jobs_list)


@student_bp.route("/jobs/<int:job_id>/apply", methods=["POST"])
@login_required
def apply(job_id):
    student_only()
    job = db.session.get(Job, job_id)
    if not job or not job.is_active:
        abort(404)
    if not job.is_student_eligible(current_user):
        flash("Your profile does not currently meet this job's listed eligibility criteria.", "warning")
        return redirect(url_for("student.jobs"))
    application = Application(student_id=current_user.id, job_id=job.id)
    db.session.add(application)
    try:
        db.session.commit()
        flash("Your application has been submitted.", "success")
    except IntegrityError:
        db.session.rollback()
        flash("You have already applied for this job.", "info")
    return redirect(url_for("student.applications"))


@student_bp.route("/student/applications")
@login_required
def applications():
    student_only()
    items = Application.query.filter_by(student_id=current_user.id).order_by(Application.applied_at.desc()).all()
    return render_template("applications.html", applications=items, admin_view=False)


@student_bp.route("/student/profile", methods=["GET", "POST"])
@login_required
def profile():
    student_only()
    if request.method == "POST":
        current_user.full_name = request.form.get("full_name", "").strip() or current_user.full_name
        current_user.department = request.form.get("department", "").strip()
        try:
            year = request.form.get("graduation_year", "").strip()
            cgpa = request.form.get("cgpa", "").strip()
            current_user.graduation_year = int(year) if year else None
            current_user.cgpa = float(cgpa) if cgpa else None
            if current_user.cgpa is not None and not 0 <= current_user.cgpa <= 10:
                raise ValueError
        except ValueError:
            db.session.rollback()
            flash("Please enter a valid year and CGPA (0 to 10).", "danger")
            return render_template("profile.html")
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("student.profile"))
    return render_template("profile.html")
