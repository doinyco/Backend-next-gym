# from unittest.mock import DEFAULT
from app import db

class History(db.Model):
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Integer)
    place_name = db.Column(db.String(100))
    time_spent = db.Column(db.String(20))
    mood = db.Column(db.String(70))
    comments = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    user = db.relationship("User", back_populates="histories")