from flask import Flask, render_template, request, flash, redirect, session
from forms import AddUserForm, LoginForm, UpdateUserForm
from models import db, connect_db, User, APIFontStyle
import requests
from api_keys import GOOGLE_API_KEY

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_1_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'somethingsecret'

connect_db(app)
db.create_all()





# res = requests.get('https://www.googleapis.com/webfonts/v1/webfonts', params={"key": GOOGLE_API_KEY})

# data = res.json()

# for item in data['items']:
#     print(item['family'], item['variants'])


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = AddUserForm()

    if form.validate_on_submit():
        full_name = form.full_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user = User.register(full_name, username, email,  password)
        
        flash('Welcome! Successfully created your account!')

        db.session.add(new_user)
        db.session.commit()

        return redirect('/')
        
    else:
        return render_template('register.html', form=form)



@app.route('/')
def home_page():
    """Render home page"""

    return render_template("home.html")


