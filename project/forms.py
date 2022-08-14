from tokenize import String
from flask_wtf import FlaskForm
# from flask_colorpicker import colorpicker
from wtforms import StringField, PasswordField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from wtforms.widgets import ColorInput
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

class NewStyleGuideForm(FlaskForm):
    """Form for adding a title to start a new styleguide """

    title = StringField('Style Guide Title', validators=[DataRequired()])
    primary_typeface = SelectField('primary_typeface', choices=[])


class ColorSchemeForm(FlaskForm):
    """Form for defining user's color scheme for style guide"""

    primary_dark = StringField('Primary Dark', widget=ColorInput())
    primary_light = StringField('Primary Light', widget=ColorInput())
    accent_1 = StringField('Accent 1', widget=ColorInput())
    accent_2 = StringField('Accent 2', widget=ColorInput())


class PrimaryTypefaceForm(FlaskForm):
    """Form for defining typeface for the style guide """
    primary_typeface = SelectField('primary_typeface', choices=[])


class TypesettingForm(FlaskForm):
    """
    Form for defining typeface and typesetting for style guide.
    
    Would like this to automatically add id to styleguide for a chosen font style once submitted (ie. for H1, H2, etc)

    """
    variant = SelectField('variant', choices=[])

    text_size = IntegerField('Text Size', validators=[
        NumberRange(min=10, max=110)
            ])

    text_transform = SelectField('text-transform', choices=[
        ('placeholder', 'Text Transform'), 
        ('none', 'None'), 
        ('uppercase', 'UPPERCASE'), 
        ('capitalize', 'Capitalize'), 
        ('lowercase', 'lowercase')])

    style_ref = StringField('style_ref')



class DeleteStyleGuideForm(FlaskForm):
    """Intentionally blank"""

