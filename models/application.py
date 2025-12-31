from extensions import db

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    applied_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
