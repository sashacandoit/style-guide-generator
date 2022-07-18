from app import app
from models import db, User, APIFontStyle

db.drop_all()
db.create_all()

username = 'sashacandoit'
full_name = 'Sasha C'
email = 'sasha@email.com'
password = 'password'

user1 = User.register(username, full_name, email,  password)


db.session.add(user1)
db.session.commit()


