

from apps import db

class Building(db.Model):
    __tablename__ = 'Building'

    id = db.Column(db.Integer, primary_key=True)
    buildingname = db.Column(db.String)
    electricity = db.Column(db.Float)
    water = db.Column(db.Float)
    assassment = db.Column(db.Int)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)


