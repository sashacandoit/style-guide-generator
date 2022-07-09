from flask import Flask, render_template, request, flash, redirect, session
from forms import AddUserForm, LoginForm, UpdateUserForm
from models import db, connect_db, User, APIFontStyle
import requests
from api_keys import GOOGLE_API_KEY

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_1_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'somethingsecret'

connect_db(app)
# db.create_all()





# res = requests.get('https://www.googleapis.com/webfonts/v1/webfonts', params={"key": GOOGLE_API_KEY})

# data = res.json()

# for item in data['items']:
#     print(item['family'], item['variants'])


@app.route('/')
def home_page():
    """Render home page"""
    
    return render_template("home.html")



@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = AddUserForm()

    if form.validate_on_submit():
        full_name = form.full_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user = User.register(full_name, username, email,  password)

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        flash('Welcome! Successfully created your account!')
        return redirect('/')
        
    else:
        return render_template('register.html', form=form)




@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        
        #Check if use passes authentication:
        if user:
            flash(f"Welcome Back, {user.full_name}!", "primary")
            session['user_id'] = user.id
            return redirect('/')
          
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)



@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("See you soon!", "info")
    return redirect('/login')