import os
from flask import Flask, render_template, request, flash, redirect, session
from sqlalchemy.exc import IntegrityError
# from forms import UserAddForm, LoginForm, UserUpdateForm
from models.user_model import db, connect_db, User
import requests
from api_keys import GOOGLE_API_KEY

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_1_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'somethingsecret'

connect_db(app)





# res = requests.get('https://www.googleapis.com/webfonts/v1/webfonts', params={"key": GOOGLE_API_KEY})

# data = res.json()

# for item in data['items']:
#     print(item['family'], item['variants'])



@app.route('/')
def home_page():
    """Render home page"""

    return render_template("home.html")


