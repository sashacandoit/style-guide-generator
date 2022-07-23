from tokenize import String
from flask_wtf import FlaskForm
# from flask_colorpicker import colorpicker
from wtforms import StringField, PasswordField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange
# from wtforms_components import ColorField
# from wtforms.fields import ColorField
import email_validator



#############################################################
#USER FORMS
#############################################################

class AddUserForm(FlaskForm):
    """Form for adding new users"""

    username = StringField('Username', validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """User Login form"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UpdateUserForm(FlaskForm):
    """Form for updating user profile"""

    username = StringField('Username')
    fullname = StringField('Full Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[Email()])
    
    password = PasswordField('Current Password')


class DeleteForm(FlaskForm):
    """Intentionally blank"""



#############################################################
#STYLE GUIDE FORMS
#############################################################

class StyleGuideTitleForm(FlaskForm):
    """Form for adding a title to start a new styleguide """

    title = StringField('Style Guide Title', validators=[DataRequired()])


class ColorSchemeForm(FlaskForm):
    """Form for defining user's color scheme for style guide"""

    primary_dark = SubmitField('Primary Dark')
    primary_light = SubmitField('Primary Light')
    accent_1 = SubmitField('Accent 1')
    accent_2 = SubmitField('Accent 2')

class PrimaryTypefaceForm(FlaskForm):
    """Form for defining typeface for the style guide """
    primary_typeface = SelectField('primary_typeface', choices=[])


class TypesettingForm(FlaskForm):
    """
    Form for defining typeface and typesetting for style guide.
    
    Would like this to automatically add id to styleguide for a chosen font style once submitted (ie. for H1, H2, etc)

    """
    variant = SelectField('variant', choices=['Font Weight', 'choose'])
    text_size = IntegerField('Text Size', validators=[
        NumberRange(min=10, max=110)
            ])

    text_transform = SelectField('text-transform', choices=[
        ('placeholder', 'Text Transform'), 
        ('none', 'None'), 
        ('uppercase', 'UPPERCASE'), 
        ('capitalize', 'Capitalize'), 
        ('lowercase', 'lowercase')])

    style_ref = SelectField('style_ref', choices=[
        ('h1', 'Display - H1'),
        ('h2', 'Header - H2'),
        ('h3', 'Title - H3'),
        ('h4', 'Subheader - H4'),
        ('h5', 'Headline - H5'),
        ('h6', 'Button - H6'),
        ('p', 'Body - P')
    ])


class StyleGuide():
    def __init__(self, forms):

        self.forms = forms


user_style_guide = StyleGuide([
    ColorSchemeForm(),
    PrimaryTypefaceForm(),
    TypesettingForm(style_ref='h1'),
    TypesettingForm(style_ref='h2'),
    TypesettingForm(style_ref='h3'),
    TypesettingForm(style_ref='h4'),
    TypesettingForm(style_ref='h5'),
    TypesettingForm(style_ref='h6'),
    TypesettingForm(style_ref='p')
])

    
