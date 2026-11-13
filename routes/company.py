from flask import Blueprint, render_template
from flask_login import login_required
from models import Company


company_bp = Blueprint("company", __name__)


@company_bp.route("/companies")
@login_required
def directory():
    companies = Company.query.order_by(Company.name).all()
    return render_template("company_directory.html", companies=companies)
