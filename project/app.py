from flask import Flask, render_template, request, flash, redirect, session
from flask_colorpicker import colorpicker

from forms import AddUserForm, LoginForm, UpdateUserForm, DeleteForm, TypesettingForm, NewStyleGuideForm, ColorSchemeForm
from models import db, connect_db, User, get_all_fonts, StyleGuide, TypesettingStyle, TypefaceVariant, get_typeface_variants, StyleRef
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
    style_guides = StyleGuide.query.filter_by(username=username).all()
    form = DeleteForm()

    return render_template('user_profile.html', user=user, form=form, style_guides=style_guides)



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

        # adds new style guide to session
        session['style_guide'] = new_style_guide.id
        style_tag = 'p'
        session['current_state'] = style_tag

        # adds primary typeface variants to database
        variants = get_typeface_variants(new_style_guide.id, primary_typeface)
        for variant in variants:
            new_variant = TypefaceVariant.add_variant(
                style_guide_id=variant['style_guide_id'],
                font_family=variant['font_family'],
                category=variant['category'],
                weight=variant['weight'],
                style=variant['style'],
                url=variant['url']
            )

            db.session.add(new_variant)
            db.session.commit()

        # redirects to first step/form page 
        return redirect(f"/style-guide/{new_style_guide.id}/typesetting/{session['current_state']}")

    # renders start page with style guide title form
    return render_template('style_guide_new.html', user=user, form=form)


##################################
# TYPESETTING ROUTES
##################################

def getTypesettingData(style_guide, tag_type):
    # gets typesetting description
    style_ref_details = StyleRef.query.get(tag_type)
    print('**********************************')
    print(f'1 - {style_ref_details}')
    print('**********************************')

    # gets variants for primary typeface
    primary_typeface = style_guide.primary_typeface
    variants = TypefaceVariant.query.filter_by(style_guide_id=style_guide.id)

    # adds starting data to TypesettingForm 
    form = TypesettingForm()
    style_ref = style_ref_details.id

    # gets variant select field choices
    v_choices = []
    for variant in variants:
        v = (variant.weight + '-' + variant.style)
        v_choices.append(v)
    form.variant.choices = v_choices

    return style_ref_details, primary_typeface, variants, form, style_ref



@app.route('/style-guide/<style_guide_id>/typesetting/<current_state>', methods=["GET", "POST"])
def typesetting_styles(style_guide_id, current_state):
    """defines typesetting style for current style with TypeSettingForm using variants from primary typeface in style guide """

    # retrieves style guide id from session 
    style_guide = StyleGuide.query.get(style_guide_id)

    #checks that user is authorized to work with style guide
    if style_guide.username != session['username'] or "username" not in session:
        flash('Sorry, you are not authorized to view that page')
        return redirect('/')

    # check session for current form state
    if "current_state" not in session:
        session['current_state'] = 'p'


    style_ref_details, primary_typeface, variants, form, style_ref = getTypesettingData(style_guide, session['current_state'])
    
    #retrieve form data on submit and add to database
    if form.validate_on_submit():
        variant=form.variant.data
        text_size= form.text_size.data
        text_transform = form.text_transform.data

        typesetting = TypesettingStyle(style_guide_id=style_guide_id, typeface=primary_typeface, variant=variant, text_size=text_size, text_transform=text_transform, style_ref=style_ref)

        db.session.add(typesetting)
        db.session.commit()
        
        # list of typesetting styles to generate form for
        form_flows = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

        # check which style tag is next in the list, or if list is complete
        if form_flows.index(session['current_state']) + 1 < len(form_flows):
            style_tag = form_flows[form_flows.index(style_ref) + 1]
            
            session['current_state'] = style_tag

            #redirects to next style tag TypesettingForm
            return redirect(f"/style-guide/{style_guide_id}/typesetting/{style_tag}")

        # typesetting forms finished - load next form page
        return redirect(f"/style-guide/{style_guide_id}/color-scheme")

    # renders page with Typesetting Form and variants
    return render_template('style_guide_typesetting.html', style_guide=style_guide, form=form, style_ref=style_ref_details, variants=variants)



##################################
# COLOR SCHEME ROUTE
##################################

@app.route('/style-guide/<style_guide_id>/color-scheme', methods=["GET", "POST"])
def color_scheme(style_guide_id):
    # retrieves style guide id from session 
    style_guide = StyleGuide.query.get(style_guide_id)
    form = ColorSchemeForm()
    if not form.primary_light.data:
        form.primary_light.data = '#F2F2F2'
    if not form.accent_1.data:
        form.accent_1.data = '#94C6F2'
    if not form.accent_2.data:
        form.accent_2.data = '#F2EEAC'

    #checks that user is authorized to work with style guide
    if style_guide.username != session['username'] or "username" not in session:
        flash('Sorry, you are not authorized to view that page')
        return redirect('/')

    #retrieve form data on submit and add to database
    if form.validate_on_submit():
        style_guide.primary_dark_color = form.primary_dark.data
        style_guide.primary_light_color = form.primary_light.data
        style_guide.accent_1_color = form.accent_1.data
        style_guide.accent_2_color = form.accent_2.data

        print('*******************************')
        print(form.primary_dark.data, form.primary_light.data, form.accent_1.data, form.accent_2.data)
        print('*******************************')
        db.session.commit()
        return redirect(f"/style-guide/{style_guide_id}")

    return render_template('style_guide_color_scheme.html', style_guide=style_guide, form=form)


@app.route('/style-guide/<style_guide_id>')
def view_style_guide(style_guide_id):
    style_guide = StyleGuide.query.get(style_guide_id)

    return render_template('style_guide.html', style_guide=style_guide)




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