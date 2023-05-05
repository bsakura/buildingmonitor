

from apps import db

class Buildings(db.Model):
    __tablename__ = 'Buildings'

    building_id = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)


