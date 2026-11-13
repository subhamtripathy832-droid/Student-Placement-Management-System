from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import current_user
from extensions import db, login_manager, csrf
from config import Config


def create_app(config_class=Config):
    load_dotenv()
    project_root = Path(__file__).resolve().parent.parent
    app = Flask(__name__, template_folder=str(project_root / "templates"), static_folder=str(project_root / "static"))
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Import models before registering routes so SQLAlchemy knows all tables.
    from models import User  # noqa: F401
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.admin import admin_bp
    from routes.company import company_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)

    @app.route("/")
    def index():
        from flask import render_template
        return render_template("index.html")

    @app.context_processor
    def inject_site_name():
        return {"site_name": "Campus Placement Portal"}

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    return app
