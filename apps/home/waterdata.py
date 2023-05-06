from apps import db 

class Water(db.Model):
    ____tablename__ = 'Water'

    building_id = db.Column(db.Integer, primary_key=True, foreign_key=True)
    date = db.Column(db.Date, primary_key=True, foreign_key=True)
    water_usage = db.Column(db.Float)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)