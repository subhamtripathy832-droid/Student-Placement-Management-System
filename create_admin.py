"""Create an administrator account from environment variables.

Set ADMIN_NAME, ADMIN_EMAIL and ADMIN_PASSWORD in your .env file first.
Run: python create_admin.py
"""
import os
from app import create_app
from extensions import db
from models import User

app = create_app()
with app.app_context():
    name = os.getenv("ADMIN_NAME", "").strip()
    email = os.getenv("ADMIN_EMAIL", "").strip().lower()
    password = os.getenv("ADMIN_PASSWORD", "")
    if not name or not email or len(password) < 12:
        raise SystemExit("Set ADMIN_NAME, ADMIN_EMAIL and ADMIN_PASSWORD (at least 12 characters) in .env first.")
    if User.query.filter_by(email=email).first():
        raise SystemExit("An account with this email already exists.")
    admin = User(full_name=name, email=email, role="admin")
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print(f"Administrator account created for {email}.")
