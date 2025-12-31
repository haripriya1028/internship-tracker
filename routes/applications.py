from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import date
from extensions import db
from models.application import Application

applications = Blueprint("applications", __name__)

@applications.route("/add", methods=["GET", "POST"])
@login_required
def add_application():
    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]
        notes = request.form["notes"]

        app = Application(
            company=company,
            role=role,
            status=status,
            applied_date=date.today(),
            notes=notes,
            user_id=current_user.id
        )

        db.session.add(app)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("add_application.html")
