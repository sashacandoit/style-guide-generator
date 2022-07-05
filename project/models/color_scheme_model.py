from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import webcolors 
from webcolors import name_to_rgb, hex_to_rgb

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
        default="0,0,0"
    )

    secondary = db.Column(
        db.Text,
        nullable=False,
        default="255,255,255"
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


    def convert_color_to_rgb(self, color):
        """Convert a color name or hex value to rbg value"""

        def hex_to_rgb():
            rgb = hex_to_rgb(color)
            print(rgb)
            return rgb

        def name_to_rgb():
            rgb = name_to_rgb(color)
            print(rgb)
            return rgb

        for func in [hex_to_rgb, name_to_rgb]:
            try:
                func(color)
                break
            except Exception as err:
                print (err, f"{color} is not a valid color")
                continue



    def __repr__(self):
        return f"<ColorScheme {self.user.username}-{self.id}: Primary={self.primary}, Secondary={self.secondary}, Accent_1={self.accent_1}, Accent_2={self.accent_2}, Accent_3={self.accent_3}>"


        

