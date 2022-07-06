from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class APIFontStyle(db.Model):

    ___tablename__ = 'api_font_styles'


    id = db.Column (
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    font_family = db.Column(
        db.Text,
        nullable=False
    )

    font_weight = db.Column(
        db.Text,
        nullable=False,
        default="regular"
    )

    category = db.Column(
        db.Text,
        nullable=False
    )

    italic = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    css_url = db.Column(
        db.Text
    )
