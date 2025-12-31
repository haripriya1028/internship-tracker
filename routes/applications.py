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
        app = Application(
            company=request.form["company"],
            role=request.form["role"],
            status=request.form["status"],
            notes=request.form["notes"],
            applied_date=date.today(),
            user_id=current_user.id
        )
        db.session.add(app)
        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("add_application.html")


@applications.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_application(id):
    app = Application.query.get_or_404(id)

    if app.user_id != current_user.id:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        app.company = request.form["company"]
        app.role = request.form["role"]
        app.status = request.form["status"]
        app.notes = request.form["notes"]

        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("edit_application.html", app=app)


@applications.route("/delete/<int:id>")
@login_required
def delete_application(id):
    app = Application.query.get_or_404(id)

    if app.user_id == current_user.id:
        db.session.delete(app)
        db.session.commit()

    return redirect(url_for("dashboard"))

