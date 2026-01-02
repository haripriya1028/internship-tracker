from flask import Flask
from extensions import db, login_manager
from flask_login import login_required, current_user
from models.application import Application
from flask import render_template
from flask import request

from config import Config





def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from models.user import User
    from models.application import Application
    from routes.auth import auth
    app.register_blueprint(auth)
    
    from routes.applications import applications
    app.register_blueprint(applications)



    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return "Internship Tracker is running!"


    @app.route("/dashboard")
    @login_required
    def dashboard():
        search = request.args.get("search", "")
        status_filter = request.args.get("status", "")
        sort = request.args.get("sort", "newest")  # 👈 NEW

        query = Application.query.filter_by(user_id=current_user.id)

        if search:
            query = query.filter(Application.company.ilike(f"%{search}%"))

        if status_filter:
            query = query.filter_by(status=status_filter)

        # 🔥 SORT LOGIC
        if sort == "oldest":
            query = query.order_by(Application.applied_date.asc())
        else:
            query = query.order_by(Application.applied_date.desc())

        apps = query.all()

        stats = {
            "Applied": 0,
            "OA": 0,
            "Interview": 0,
            "Offer": 0,
            "Rejected": 0
        }

        for app in apps:
            if app.status in stats:
                stats[app.status] += 1

        return render_template(
            "dashboard.html",
            applications=apps,
            stats=stats,
            search=search,
            status_filter=status_filter,
            sort=sort   # 👈 PASS TO TEMPLATE
        )





    


    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
