"""SQLAlchemy models for Capstone 1"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import requests
import json
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


    style_guides = db.relationship('StyleGuide', cascade="all,delete", backref='user')



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




class StyleGuide(db.Model):

    ___tablename__ = 'style_guides'

    id = db.Column (
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    username = db.Column(
        db.Text,
        db.ForeignKey('user.username', ondelete='CASCADE'), nullable=False
    )

    title = db.Column(
        db.Text,
        unique=True
    )

    primary_typeface = db.Column(
        db.Text
    )

    variants = db.relationship('TypefaceVariant', cascade="all,delete", backref='style_guide')

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

    typesetting_styles = db.relationship("TypesettingStyle", cascade="all,delete", backref='style_guide')


    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )



class TypefaceVariant(db.Model):
    __tablename__ = 'typeface_variants'

    id = db.Column (
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    style_guide_id = db.Column(
        db.Integer,
        db.ForeignKey('style_guide.id', ondelete='CASCADE'),
        nullable=False)

    font_family = db.Column(
        db.Text
    )

    category = db.Column(
        db.Text
    )

    weight = db.Column(
        db.Text
    )

    style = db.Column(
        db.Text
    )

    url = db.Column(
        db.Text
    )

    @classmethod
    def add_variant(cls, style_guide_id, font_family, category, weight, style, url):
        """
        Add primary font variants to database
        """

        new_variant = TypefaceVariant(
            style_guide_id=style_guide_id,
            font_family=font_family,
            category=category,
            weight=weight,
            style=style,
            url=url
        )

        db.session.add(new_variant)
        return new_variant


def get_all_fonts():
    res = requests.get('https://www.googleapis.com/webfonts/v1/webfonts', params={"key": GOOGLE_API_KEY})

    data = res.json()

    all_fonts = []

    for item in data['items']:
        all_fonts.append((item['family'], item['family']))

    print(all_fonts)
    return all_fonts
    

def get_typeface_variants(style_guide_id, typeface):
    res = requests.get('https://www.googleapis.com/webfonts/v1/webfonts', params={"key": GOOGLE_API_KEY})

    data = res.json()

    base_url = 'https://fonts.googleapis.com/css?family='
    base_url = base_url + (typeface.replace(" ", "+"))
    typeface_variants = []

    for item in data['items']:
        
        if item['family'] == typeface:
            category = item['category']

            for variant in item['variants']:
                variant_url = base_url + ':' + variant

                if variant == 'italic':
                    weight = '400'
                    style = 'italic'

                    typeface_variant = dict(
                        style_guide_id=style_guide_id,
                        font_family=typeface,
                        category=category,
                        weight=weight,
                        style=style,
                        url=variant_url
                        )
                    
                    typeface_variants.append(typeface_variant)

                
                elif variant == 'regular':
                    weight = '400'
                    style = 'normal'

                    typeface_variant = dict(
                        style_guide_id=style_guide_id,
                        font_family=typeface,
                        category=category,
                        weight=weight,
                        style=style,
                        url=variant_url
                        )
                    
                    typeface_variants.append(typeface_variant)

                elif 'italic' in variant:
                    weight = variant.removesuffix('italic')
                    style = 'italic'

                    typeface_variant = dict(
                        style_guide_id=style_guide_id,
                        font_family=typeface,
                        category=category,
                        weight=weight,
                        style=style,
                        url=variant_url
                        )
                    
                    typeface_variants.append(typeface_variant)


                else:
                    weight = variant
                    style = 'normal'

                    typeface_variant = dict(
                        style_guide_id=style_guide_id,
                        font_family=typeface,
                        category=category,
                        weight=weight,
                        style=style,
                        url=variant_url
                        )
                    
                    typeface_variants.append(typeface_variant)
                
    print(typeface_variants)
    return typeface_variants




class TypesettingStyle(db.Model):

    ___tablename__ = 'typesetting_styles'
    

    id = db.Column (
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    style_guide_id = db.Column(
        db.Integer,
        db.ForeignKey('style_guide.id', ondelete='CASCADE'),
        nullable=False)


    typeface = db.Column(
        db.Text
    )

    font_weight = db.Column(
        db.Text
    )

    font_style = db.Column(
        db.Text
    )

    text_size = db.Column(
        db.Integer
    )

    text_transform = db.Column(
        db.Text, 
        default=None
    )

    style_ref = db.Column(
        db.Text, 
        db.ForeignKey('style_ref.id', ondelete='CASCADE')
    )

    style_ref_details = db.relationship("StyleRef")





class StyleRef(db.Model):
    ___tablename__ = 'style_refs'

    id = db.Column (
        db.Text,
        primary_key=True
    )

    name = db.Column (
        db.Text
    )

    description = db.Column (
        db.Text
    )

    uses = db.Column (
        db.Text
    )

    colors = db.relationship("StyleColor")
    


class StyleColor(db.Model):
    __tablename__ = 'style_colors'

    id = db.Column (
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    style_ref = db.Column(
        db.Text, 
        db.ForeignKey('style_ref.id', ondelete='CASCADE')
    )

    color = db.Column(
        db.Text
    )


    @classmethod
    def add_pair(cls, style_ref, color):
        pair = StyleColor(
            style_ref=style_ref,
            color=color
        )

        db.session.add(pair)
        return pair



def format_datetime():
    date_time = datetime.utcnow()
    format_date = date_time.strftime("%d %B, %Y")
    return format_date


