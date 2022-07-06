from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FontStyle(db.Model):

    ___tablename__ = 'font_styles'

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

    user = db.relationship('User', backref='font_styles')

    font_family = db.Column(
        db.Text,
        nullable=False,
        default="sans-serif"
    )

    font_weight = db.Column(
        db.Integer,
        nullable=False,
        default="regular"
    )

    font_style = db.Column(
        db.Text,
        nullable=False,
        default=None
    )

    font_file = db.Column(
        db.Text,
        nullable=False
    )

    font_transform = db.Column(
        db.Text,
        nullable=False,
        default=None
    )

    font_size = db.Column(
        db.Integer,
        nullable=False,
        default=16
    )

    font_color = db.Column(
        db.Text,
        nullable=False,
        default="primary"
    ) # Should this reference the color_schemes table?


    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )

