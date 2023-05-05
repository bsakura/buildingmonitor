from apps import db 

class Leed(db.Model):
    __tablename__ = 'Leed'

    building_id = db.Column(db.Integer, primary_key=True, foreign_key=True)
    location_transportation = db.Column(db.Integer)
    sustainable_sites = db.Column(db.Integer)
    water_efficiency = db.Column(db.Integer)
    energy_atmosphere = db.Column(db.Integer)
    materials_resources = db.Column(db.Integer)
    indoor_environmental_quality = db.Column(db.Integer)
    innovation = db.Column(db.Integer)
    total_leed = db.Column(db.Integer)
    date = db.Column(db.Date, primary_key=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)