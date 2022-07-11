from app import app
from models import db, User

db.drop_all()
db.create_all()

user1 = User(
    username="laurak",
    full_name="Laura Corbin",
    email="laura@email.com",
    password="password"
)

user2 = User(
    username="jessczer",
    full_name="Jessica C",
    email="jessica@email.com",
    password="password"
)

db.session.add_all([user1, user2])
db.session.commit()

# Should I add my API fonts to the API Font table from here?