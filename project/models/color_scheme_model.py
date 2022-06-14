from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import webcolors 

db = SQLAlchemy()



class ColorScheme(db.Model):

    ___tablename__ = 'color_schemes'

    id = db.Column (
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    user = db.relationship('User', backref='color_schemes')

    primary = db.Column(
        db.Text,
        nullable=False,
        default="000000"
    )

    secondary = db.Column(
        db.Text,
        nullable=False,
        default="ffffff"
    )

    acccent_1 = db.Column(
        db.Text,
        nullable=False,
        default=None
    )

    acccent_2 = db.Column(
        db.Text,
        nullable=False,
        default=None
    )

    acccent_3 = db.Column(
        db.Text,
        nullable=False,
        default=None
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )
