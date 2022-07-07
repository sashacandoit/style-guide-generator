from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint
from api_font_model import APIFontStyle

db = SQLAlchemy()


class UserFontStyle(db.Model):

    ___tablename__ = 'user_font_styles'

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

    user = db.relationship('User', backref='user_font_styles')


    font_family = db.Column(
        db.Text,
        db.ForeignKey('api_font_styles.font_family')
    )

    font_variant = db.Column(
        db.Text,
        db.ForeignKey('api_font_styles.variant')
    )

    # __table_args__ = (ForeignKeyConstraint(
    #     [font_family, font_variant],
    #     [APIFontStyle.font_family, APIFontStyle.variant]
    # ))

    uppercase = db.Column(
        db.Boolean,
        default=False
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

