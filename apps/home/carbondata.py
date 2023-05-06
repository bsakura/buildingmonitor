from apps import db 

class Carbon(db.Model):
    ____tablename__ = 'Carbon'

    building_id = db.Column(db.Integer, primary_key=True, foreign_key=True)
    date = db.Column(db.Date, primary_key=True, foreign_key=True)
    carbon_footprint = db.Column(db.Float)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)