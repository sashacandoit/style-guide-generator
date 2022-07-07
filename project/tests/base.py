import os
from unittest import TestCase
from project.models.color_scheme_model import ColorScheme
from project.models.user_model import User
from project.models.font_style_model import FontStyle
from project.models.style_guide_model import Styleguide

os.environ['DATABASE_URL'] = "postgresql:///style_guide_maker_test"

from project import app, db


class BaseTestCase(TestCase):
    """
    Base test case to use with all tests -
    setUp and tearDown for all tests
    """

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app


    """Create app and add all tables with sample data"""
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

        db.session.add(
            FontStyle(
                dict(
                    font_family="sans-serif",
                    font_weight=400,
                    font_style="normal",
                    font_size=18,
                    font_color="primary"
                )
            ))

        # db.session.add(
        #     StyleGuide(
        #         dict(
        #             title="Test Style Guide",
        #             color_scheme_id="",
        #             p="",
        #             h1="",
        #             h2="",
        #             h3="",
        #             h4="",
        #             h5="",
        #             h6=""
        #         )
        #     ))

        db.session.commit()

    
    """Clear sample data from each table after each test"""
    def tearDown(self):
        db.session.remove()
        db.drop_all()