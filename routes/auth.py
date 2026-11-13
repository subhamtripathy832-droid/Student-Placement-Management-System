from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("student.dashboard" if current_user.role == "student" else "admin.dashboard"))
    if request.method == "POST":
        name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        department = request.form.get("department", "").strip()
        year_text = request.form.get("graduation_year", "").strip()
        cgpa_text = request.form.get("cgpa", "").strip()
        if not name or not email or len(password) < 8:
            flash("Enter your name and email, and use a password of at least 8 characters.", "danger")
            return render_template("register.html")
        try:
            year = int(year_text) if year_text else None
            cgpa = float(cgpa_text) if cgpa_text else None
            if cgpa is not None and not 0 <= cgpa <= 10:
                raise ValueError
        except ValueError:
            flash("Enter a valid graduation year and CGPA (0 to 10).", "danger")
            return render_template("register.html")
        user = User(full_name=name, email=email, department=department, graduation_year=year, cgpa=cgpa, role="student")
        user.set_password(password)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("An account with that email already exists.", "danger")
            return render_template("register.html")
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("student.dashboard" if current_user.role == "student" else "admin.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Welcome back!", "success")
            next_page = request.args.get("next")
            # Only allow local relative redirects.
            if next_page and next_page.startswith("/") and not next_page.startswith("//"):
                return redirect(next_page)
            return redirect(url_for("student.dashboard" if user.role == "student" else "admin.dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
