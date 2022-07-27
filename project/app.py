from flask import Flask, render_template, request, flash, redirect, session
from flask_colorpicker import colorpicker

from forms import AddUserForm, LoginForm, UpdateUserForm, DeleteForm, ColorSchemeForm, TypesettingForm, NewStyleGuideForm
from models import db, connect_db, User, APIFontStyle, get_all_fonts, StyleGuide, TypesettingStyle, TypefaceVariant, get_typeface_variants, get_variant_urls, get_variant_choices
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_1_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'somethingsecret'

connect_db(app)



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

@app.route('/users/<username>/style-guide/new', methods=["GET", "POST"])
def start_new_styleguide(username):
    """Starts a session when user starts new style guide by giving it a title redirects to first step/form page"""

    # checks if user is in session
    if username != session['username'] or "username" not in session:
        flash('Sorry, you are not authorized to view that page')
        return redirect('/')

    form = NewStyleGuideForm()
    user = User.query.get(username)
    all_fonts = get_all_fonts()
    form.primary_typeface.choices = all_fonts

    # handles form submition for new style guide title
    if form.validate_on_submit():
        title = form.title.data
        primary_typeface = form.primary_typeface.data
        new_style_guide = StyleGuide(username=session["username"], title=title, primary_typeface=primary_typeface)

        # adds title to database assigned to new styleguide assigned to that user
        db.session.add(new_style_guide)
        db.session.commit()

        # adds FORMS to session with no submitions
        session['style_guide'] = new_style_guide.id

        variants = get_typeface_variants(new_style_guide.id, primary_typeface)
        for variant in variants:
            new_variant = TypefaceVariant.add_variant(
                style_guide_id=variant.style_guide_id,
                font_family=variant.font_family,
                category=variant.category,
                weight=variant.weight,
                style=variant.style,
                url=variant.url
            )

            db.session.add(new_variant)
            db.session.commit()

        # redirects to first step/form page 
        return redirect(f"/style-guide/{new_style_guide.id}/typesetting/body")

    # renders start page with stype guide title form
    return render_template('style_guide_new.html', user=user, form=form)


##################################
# TYPESETTING ROUTES
##################################


@app.route('/style-guide/<style_guide_id>/typesetting/body')
def typesetting_body(style_guide_id):

    style_guide = StyleGuide.query.get(style_guide_id)

    if style_guide.username != session['username'] or "username" not in session:
        flash('Sorry, you are not authorized to view that page')
        return redirect('/')

    form = TypesettingForm()
    primary_typeface = style_guide.primary_typeface
    style_ref = 'p'
    form.variant.choices = get_variant_choices(primary_typeface)


    if form.validate_on_submit():
        variant=form.variant.data
        text_size= form.text_size.data
        text_transform = form.text_transform.data

        body_typesetting = TypesettingStyle(style_guide_id=style_guide_id, typeface=primary_typeface, variant=variant, text_size=text_size, text_transform=text_transform, style_ref=style_ref)

        db.session.add(body_typesetting)
        db.session.commit()

        return redirect(f"/style-guide/{style_guide_id}/typesetting/h1")

        
    return render_template('style_guide_typesetting.html', style_guide=style_guide, form=form)












# @app.route('/style-guide/color-scheme')
# def view_style_guide():
#     color_form = ColorSchemeForm()
#     if color_form.validate_on_submit():
#         primary_dark = color_form.primary_dark.data
#         return primary_dark
#     return render_template('new_style_guide.html', form=color_form)


# @app.route('users/<username>/style-guide/new', methods=["GET", "POST"])
# def start_new_styleguide(username):
#     """Starts a session when user starts new style guide by giving it a title redirects to first step/form page"""

#     # checks if user is in session
#     if username != session['username'] or "username" not in session:
#         flash('Sorry, you are not authorized to view that page')
#         return redirect('/')

#     with app.app_context():

#         form = StyleGuideTitleForm()
#         user = User.query.get(username)

#         # handles form submition for new style guide title
#         if form.validate_on_submit():
#             title = form.title.data
#             new_style_guide = StyleGuide(username=session["username"], title=title)

#             # adds title to database assigned to new styleguide assigned to that user
#             db.session.add(new_style_guide)
#             db.session.commit()

#             # adds FORMS to session with no submitions
#             session[FORMS] = []
#             # redirects to first step/form page 
#             return redirect("/new/0")

#     # renders start page with stype guide title form
#     return render_template('style-guide/new.html', user=user, form=form)


# @app.route('/style-guide/new/<int:form_id>', methods=["GET"])
# def start_style_guide_forms(form_id):
#     """Shows the next form in sequence for new style guide"""

#     #get forms already submitted
#     submissions = session.get(FORMS)

#     print('***************************************')
#     print(session(FORMS))
#     print('***************************************')

#     if (submissions == None):
#         #if session not started, redirect to home
#         return redirect('/')

#     if (len(submissions) == len(user_style_guide.forms)):
#         #style guide forms completed - redirect to home
#         return redirect('/')

#     if (len(submissions) != form_id):
#         #user accessing forms out of order
        
#         flash("Please answer questions in order")

#         #return user to correct from in sequence
#         return redirect(f'/style-guide/new/{len(submissions)}')

#     form = user_style_guide.forms[form_id]
#     return render_template('style-guide/new.html', form_id=form_id, form=form)



# @app.route('/style-guide/typeface')
# def set_typeface():
#     form = PrimaryTypefaceForm()
#     all_fonts = get_all_fonts()
#     form.primary_typeface.choices = all_fonts
        
#     return render_template('typeface_form.html', form=form)