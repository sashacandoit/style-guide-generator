from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class APIFontStyle(db.Model):

    ___tablename__ = 'api_font_styles'

    font_family = db.Column(
        db.Text,
        primary_key=True,
        nullable=False
    )

    variant = db.Column(
        db.Text,
        nullable=False,
        primary_key=True,
        default="regular"
    )

    category = db.Column(
        db.Text,
        nullable=False
    )

    css_url = db.Column(
        db.Text
    )
