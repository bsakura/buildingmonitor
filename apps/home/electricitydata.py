from apps import db

class Electricity(db.Model):
    __tablename__ = 'Electricity'

    building_id = db.Column(db.Integer, primary_key=True, foreign_key=True)
    date = db.Column(db.Date, primary_key=True, foreign_key=True)
    electricity_usage = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)