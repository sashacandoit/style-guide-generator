import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from project.models.color_scheme_model import User, ColorScheme, StyleGuide, FontStyle

os.environ['DATABASE_URL'] = "postgresql:///style_guide_maker_test"

from project import app, db


class BaseTestCase(TestCase):
    """Base test case to use with all tests"""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(
            User(
                dict(
                    full_name="Test User",
                    username="testuser",
                    email="testuser@email.com",
                    password="password"
                )))

        db.session.add(
            ColorScheme(
                dict(
                    primary="000000",
                    secondary="ffffff",
                    accent_1="red",
                    accent_2="blue",
                    accent_3="green"
                )
            ))


        db.session.commit()