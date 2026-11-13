from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required
from extensions import db
from models import User, Company, Job, Application, PlacementRecord


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_only():
    if current_user.role != "admin":
        abort(403)


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    admin_only()
    stats = {
        "students": User.query.filter_by(role="student").count(),
        "companies": Company.query.count(),
        "jobs": Job.query.count(),
        "applications": Application.query.count(),
        "placements": PlacementRecord.query.count(),
    }
    recent = Application.query.order_by(Application.applied_at.desc()).limit(8).all()
    return render_template("admin_dashboard.html", stats=stats, applications=recent)


@admin_bp.route("/students")
@login_required
def students():
    admin_only()
    students_list = User.query.filter_by(role="student").order_by(User.full_name).all()
    return render_template("students.html", students=students_list)


@admin_bp.route("/companies", methods=["GET", "POST"])
@login_required
def companies():
    admin_only()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Company name is required.", "danger")
        else:
            company = Company(name=name, website=request.form.get("website", "").strip(),
                              location=request.form.get("location", "").strip(),
                              description=request.form.get("description", "").strip())
            db.session.add(company)
            try:
                db.session.commit()
                flash("Company added.", "success")
            except Exception:
                db.session.rollback()
                flash("Could not add company. Check whether the company already exists.", "danger")
        return redirect(url_for("admin.companies"))
    company_list = Company.query.order_by(Company.name).all()
    return render_template("companies.html", companies=company_list)


@admin_bp.route("/jobs/new", methods=["GET", "POST"])
@login_required
def new_job():
    admin_only()
    companies_list = Company.query.order_by(Company.name).all()
    if request.method == "POST":
        try:
            company_id = int(request.form.get("company_id", ""))
            min_cgpa = float(request.form.get("minimum_cgpa", "0") or 0)
            graduation_year_text = request.form.get("graduation_year", "").strip()
            from datetime import datetime
            deadline_text = request.form.get("deadline", "").strip()
            job = Job(
                company_id=company_id,
                title=request.form.get("title", "").strip(),
                description=request.form.get("description", "").strip(),
                location=request.form.get("location", "").strip(),
                minimum_cgpa=min_cgpa,
                eligible_departments=request.form.get("eligible_departments", "All").strip() or "All",
                graduation_year=int(graduation_year_text) if graduation_year_text else None,
                deadline=datetime.strptime(deadline_text, "%Y-%m-%d").date() if deadline_text else None,
            )
            if not job.title or not job.description or not (0 <= min_cgpa <= 10):
                raise ValueError
            db.session.add(job)
            db.session.commit()
            flash("Job posting created.", "success")
            return redirect(url_for("admin.dashboard"))
        except (ValueError, TypeError):
            db.session.rollback()
            flash("Please check all job details and enter a valid CGPA.", "danger")
        except Exception:
            db.session.rollback()
            flash("Unable to create the job posting. Check the selected company.", "danger")
    return render_template("new_job.html", companies=companies_list)


@admin_bp.route("/applications")
@login_required
def applications():
    admin_only()
    items = Application.query.order_by(Application.applied_at.desc()).all()
    return render_template("applications.html", applications=items, admin_view=True)


@admin_bp.route("/applications/<int:application_id>/status", methods=["POST"])
@login_required
def update_application(application_id):
    admin_only()
    item = db.session.get(Application, application_id)
    if not item:
        abort(404)
    allowed = {"Submitted", "Under Review", "Shortlisted", "Selected", "Rejected"}
    status = request.form.get("status", "")
    if status not in allowed:
        flash("Invalid application status.", "danger")
    else:
        item.status = status
        db.session.commit()
        flash("Application status updated.", "success")
    return redirect(url_for("admin.applications"))
