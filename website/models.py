from enum import unique
from flask_sqlalchemy.model import Model
from . import db
from sqlalchemy.sql import func

class Run(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    time_taken = db.Column(db.Integer)
    minute_seconds = db.Column(db.String(150))
    date = db.Column(db.Date, default= func.current_date())
    username = db.Column(db.String(150))