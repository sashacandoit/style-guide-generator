from flask import Flask, render_template, request, flash, redirect, session
from flask_colorpicker import colorpicker

from forms import AddUserForm, LoginForm, UpdateUserForm, DeleteForm, ColorSchemeForm, TypesettingForm, StyleGuideTitleForm, PrimaryTypefaceForm
from models import db, connect_db, User, APIFontStyle, add_api_data, get_all_fonts, StyleGuide, UserTypeface, TypesettingStyle
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_1_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'somethingsecret'

connect_db(app)

FORMS = "forms"


#############################################################
# USER ROUTES
#############################################################

@app.route('/')
def home_page():
    """Render home page"""
    
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register_user():

    if "username" in session:
        return redirect(f"users/{session['username']}")


    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        full_name = form.full_name.data
        email = form.email.data
        password = form.password.data
        new_user = User.register(username, full_name, email,  password)

        db.session.add(new_user)
        
        try:
            db.session.commit()

        except IntegrityError:
            form.username.errors.append('Username already in use', 'warning')
            return render_template('register.html', form=form)

        session['username'] = new_user.username
        flash('Welcome to the party! Successfully created your account!')
        return redirect(f"users/{session['username']}")
        
    else:
        return render_template('register.html', form=form)




@app.route('/login', methods=['GET', 'POST'])
def login_user():

    if "username" in session:
        return redirect(f"users/{session['username']}")


    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        
        #Check if use passes authentication:
        if user:
            flash(f"Welcome Back, {user.full_name}!")
            session['username'] = user.username
            return redirect('/')
          
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)



@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("See you soon!", "primary")
    return redirect('/login')



@app.route('/users/<username>')
def show_user(username):
    
    if username != session['username'] or "username" not in session:
        flash("Sorry, you are not authorized to view that page")
        return redirect('/login')
        
    user = User.query.get(username)
    form = DeleteForm()

    return render_template('user_profile.html', user=user, form=form)



@app.route('/users/<username>/delete', methods=["GET", "POST"])
def delete_user(username):
    """Delete current user in session"""

    user = User.query.get_or_404(username)
        
    if username != session['username'] or "username" not in session:
        flash('Sorry, you are not authorized to view that page')
        return redirect('/')
        
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        session.pop("username")

    flash("User Deleted!")
    return redirect('/')



#############################################################
# STYLE GUIDE ROUTES
#############################################################

@app.route('users/<username>/style-guide/new', methods=["GET", "POST"])
def start_new_styleguide(username):
    """Starts a session when user starts new style guide by giving it a title redirects to first step/form page"""

    # checks if user is in session
    if username != session['username'] or "username" not in session:
        flash('Sorry, you are not authorized to view that page')
        return redirect('/')

    form = StyleGuideTitleForm()
    user = User.query.get(username)

    # handles form submition for new style guide title
    if form.validate_on_submit():
        title = form.title.data
        new_style_guide = StyleGuide(username=session["username"], title=title)

        # adds title to database assigned to new styleguide assigned to that user
        db.session.add(new_style_guide)
        db.session.commit()

        # adds FORMS to session with no submitions
        session[FORMS] = []
        # redirects to first step/form page 
        return redirect("/new/0")

    # renders start page with stype guide title form
    return render_template('style-guide/new.html', user=user, form=form)




@app.route('/style-guide/typeface')
def set_typeface():
    form = PrimaryTypefaceForm()
    all_fonts = get_all_fonts()
    form.primary_typeface.choices = all_fonts
        
    return render_template('typeface_form.html', form=form)


@app.route('/style-guide/typesetting')
def set_typesettings():
    form = TypesettingForm()
    all_fonts = get_all_fonts()
    # form.primary_typeface.choices = all_fonts
        
    return render_template('typesetting_form.html', form=form)


# @app.route('/style-guide/color-scheme')
# def view_style_guide():
#     color_form = ColorSchemeForm()
#     if color_form.validate_on_submit():
#         primary_dark = color_form.primary_dark.data
#         return primary_dark
#     return render_template('new_style_guide.html', form=color_form)


@app.route('/style-guide/new', methods=["GET", "POST"])
def start_style_guide():
