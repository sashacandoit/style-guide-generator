from app import app
from models import db, User

db.drop_all()
db.create_all()

user1 = User(
    full_name="Laura Corbin",
    username="laurak",
    email="laura@email.com",
    password="password"
)

user2 = User(
    full_name="Jessica C",
    username="jessczer",
    email="jessica@email.com",
    password="password"
)

db.session.add_all([user1, user2])
db.session.commit()