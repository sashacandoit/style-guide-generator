from app import app
from models import db, User, StyleGuide, TypefaceVariant, TypesettingStyle, APIFontStyle, StyleRef

db.drop_all()
db.create_all()

# Create starting user
username = 'sashacandoit'
full_name = 'Sasha C'
email = 'sasha@email.com'
password = 'password'

user1 = User.register(username, full_name, email,  password)


db.session.add(user1)
db.session.commit()



# Add style refs to database

p = StyleRef(
    id='p',
    name='Body',
    description='This is the main font used for your brand. Use this for all paragraphs, descriptions, and any large blocks of text.'
)

h1 = StyleRef(
    id='h1',
    name='Display',
    description='This is your largest typesetting. Display headers are mostly used as a Primary heading, Splash headings, and Modal titles.'
)

h2 = StyleRef(
    id='h2',
    name='Header',
    description='This is usually your second largest typesetting. Headers are mostly used for Large Section Titles and to break up content areas.'
)

h3 = StyleRef(
    id='h3',
    name='Title',
    description='Title headings are used to break up content within Large Sections. They are usually used for smaller Section Titles, Form Titles and Tabs.'
)

h4 = StyleRef(
    id='h4',
    name='Subheader',
    description='Subheaders provide suplementary descriptions for small sections. they are usually used to highlight important information, Instructions, and Table Titles'
)

h5 = StyleRef(
    id='h5',
    name='Headline',
    description='Headlines are used to highlight important blocks of text and Info Paragraphs. They are usually longer than the other headers but not as long as body content.'
)

h6 = StyleRef(
    id='h6',
    name='Buttons',
    description='Button styles are usually larger than your body content and are meant to grab the attention of users.'
)

db.session.add_all([p,h1,h2,h3,h4,h5,h6])
db.session.commit()