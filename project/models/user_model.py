from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    ___tablename__ = 'users'

    id = db.Column (
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    full_name = db.Column(
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
        return f"<User #{self.id}: {self.full_name}, {self.username}, {self.email}>"


    @classmethod
    def signup(cls, full_name, username, email, password):
        """
        Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            full_name=full_name,
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