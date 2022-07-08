from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length
import email_validator



#############################################################
#USER FORMS
#############################################################

class AddUserForm(FlaskForm):
    """Form for adding new users"""

    full_name = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """User Login form"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UpdateUserForm(FlaskForm):
    """Form for updating user profile"""

    fullname = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username')
    email = StringField('E-mail', validators=[Email()])
    
    password = PasswordField('Current Password')