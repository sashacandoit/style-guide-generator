"""SQLAlchemy models for Capstone 1"""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):

    ___tablename__ = 'users'

    id = db.Column (
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = db.Column(
        db.Text
    )

    last_name = db.Column(
        db.Text
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    style_guides = db.relationship('Style_Guide')

    font_styles = db.relationship('Font_Style')

    color_schemes = db.relationship('Color_Scheme')


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"


    @classmethod
    def signup(cls, first_name, last_name, username, email, password):
        """
        Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    


class Font_Style(db.Model):

    ___tablename__ = 'users'

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
        default="400"
    )

    font_style = db.Column(
        db.Text,
        nullable=False,
        default="Normal"
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