from flask import Flask
from extensions import db, login_manager
from flask_login import login_required, current_user
from models.application import Application
from flask import render_template


from config import Config





def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

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
        apps = Application.query.filter_by(user_id=current_user.id).all()
        return render_template("dashboard.html", applications=apps)


    


    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
