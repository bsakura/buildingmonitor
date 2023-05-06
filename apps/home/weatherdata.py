from apps import db 

class Weather(db.Model):
    ____tablename__ = 'Weather'

    date = db.Column(db.Date, primary_key=True)
    max_temperature = db.Column(db.Float)
    min_temperature = db.Column(db.Float)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)