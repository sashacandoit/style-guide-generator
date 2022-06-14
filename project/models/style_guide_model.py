from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class StyleGuide(db.Model):

    ___tablename__ = 'style_guides'

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

    user = db.relationship('User', backref='style_guides')

    title = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )

    color_scheme_id = db.Column(
        db.Integer,
        db.ForeignKey('color_schemes.id'),
        nullable=False
    )

    color_scheme = db.relationship('ColorScheme', backref='style_guides')

    p = db.Column(
        db.Integer,
        db.ForiegnKey('font_styles.id'),
        nullable=False
    )

    h1 = db.Column(
        db.Integer,
        db.ForiegnKey('font_styles.id'),
        nullable=False
    )

    h2 = db.Column(
        db.Integer,
        db.ForiegnKey('font_styles.id'),
        nullable=False
    )

    h3 = db.Column(
        db.Integer,
        db.ForiegnKey('font_styles.id'),
        nullable=False
    )

    h4 = db.Column(
        db.Integer,
        db.ForiegnKey('font_styles.id'),
        nullable=False
    )

    h5 = db.Column(
        db.Integer,
        db.ForiegnKey('font_styles.id'),
        nullable=False
    )

    h6 = db.Column(
        db.Integer,
        db.ForiegnKey('font_styles.id'),
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )

    public = db.Column(
        db.Boolean, 
        default=True,
        nullable=False
    )