from app import db

class Place(db.Model):
    place_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    maps_place_id = db.Column(db.String(80))
    name = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    user = db.relationship("User", back_populates="places")