"""SQLAlchemy models for Capstone 1"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import webcolors 
from webcolors import name_to_rgb, hex_to_rgb
import requests
from api_keys import GOOGLE_API_KEY

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)



    
class User(db.Model):

    ___tablename__ = 'users'

    username = db.Column(
        db.Text,
        primary_key=True,
        nullable=False,
        unique=True
    )

    full_name = db.Column(
        db.Text
    )

    email = db.Column(
        db.Text,
        nullable=False
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )


    user_font_styles = db.relationship('UserFontStyle', backref='user')

    # color_schemes = db.relationship('ColorScheme', backref='user')

    # style_guides = db.relationship('StyleGuide', backref='user')



    def __repr__(self):
        return f"<Username {self.username}: {self.full_name}, {self.timestamp}, {self.email}>"


    @classmethod
    def register(cls, username, full_name, email, password):
        """
        Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            full_name=full_name,
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


    
class APIFontStyle(db.Model):

    ___tablename__ = 'api_font_styles'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    font_family = db.Column(
        db.Text,
        nullable=False
    )

    variant = db.Column(
        db.Text,
        nullable=False,
        default="regular"
    )

    category = db.Column(
        db.Text,
        nullable=False
    )

    css_url = db.Column(
        db.Text
    )

    @classmethod
    def gen_font_data(cls, font_family, variant, category):
        """
        Adds font api data to the APIFontStyles table
        """

        font_style = APIFontStyle(
            font_family=font_family,
            variant=variant,
            category=category
        )

        return font_style


def add_api_data():
    res = requests.get('https://www.googleapis.com/webfonts/v1/webfonts', params={"key": GOOGLE_API_KEY})

    data = res.json()

    for item in data['items']:
        font_family = item['family']
        category = item['category']
        
        for variant in item['variants']:
            variant = variant
            font = dict(font_family=font_family, variant=variant, category=category)
            print(font)

            # api_font_style = APIFontStyle(font)
            api_font_style = APIFontStyle.gen_font_data(font_family, variant, category)
            
            db.session.add(api_font_style)
            db.session.commit()



class UserTypefaces(db.Model):
    __tablename__ = 'user_typefaces'

    id = db.Column (
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    style_guide_id = db.Column(
        db.Integer,
        db.ForiegnKey('style_guide.id')
    )

    style_guide = db.relationship('StyleGuides')

    font_family = db.Column(
        db.Text
    )

    variant = db.Column(
        db.Text
    )




class UserFontStyle(db.Model):

    ___tablename__ = 'user_font_styles'
    

    id = db.Column (
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    style_guide_id = db.Column(
        db.Integer,
        db.ForiegnKey('style_guide.id')
    )

    style_guide = db.relationship('StyleGuides')

    font_family = db.Column(
        db.Text,
        db.ForeignKey('user_typeface.font_family')
    )

    font_variant = db.Column(
        db.Text,
        db.ForeignKey('user_typeface.variant')
    )

    user_typeface = db.relationship('UserTypeface')

    text_size = db.Column(
        db.Integer
    )

    text_transform = db.Column(
        db.Text, 
        default=None
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
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )


    title = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )

    primary_dark_color = db.Column(
        db.Text
    )

    primary_light_color = db.Column(
        db.Text
    )

    accent_1_color = db.Column(
        db.Text
    )

    accent_2_color = db.Column(
        db.Text
    )

    p = db.Column(
        db.Integer,
        db.ForeignKey('user_font_styles.id')
    )

    h1 = db.Column(
        db.Integer,
        db.ForeignKey('user_font_styles.id')
    )

    h2 = db.Column(
        db.Integer,
        db.ForeignKey('user_font_styles.id')
    )

    h3 = db.Column(
        db.Integer,
        db.ForeignKey('user_font_styles.id')
    )

    h4 = db.Column(
        db.Integer,
        db.ForeignKey('user_font_styles.id')
    )

    h5 = db.Column(
        db.Integer,
        db.ForeignKey('user_font_styles.id')
    )

    h6 = db.Column(
        db.Integer,
        db.ForeignKey('user_font_styles.id')
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )

    




def format_datetime():
    date_time = datetime.utcnow()
    format_date = date_time.strftime("%d %B, %Y")
    return format_date


#     def convert_color_to_rgb(self, color):
#         """Convert a color name or hex value to rbg value"""

#         def hex_to_rgb():
#             rgb = hex_to_rgb(color)
#             print(rgb)
#             return rgb

#         def name_to_rgb():
#             rgb = name_to_rgb(color)
#             print(rgb)
#             return rgb

#         for func in [hex_to_rgb, name_to_rgb]:
#             try:
#                 func(color)
#                 break
#             except Exception as err:
#                 print (err, f"{color} is not a valid color")
#                 continue





