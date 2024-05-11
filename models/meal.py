from database import db

class Meal(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80), nullable=False, unique=True)
	description = db.Column(db.String(160))
	date_time = db.Column(db.String(20))
	on_diet = db.Column(db.Boolean())

