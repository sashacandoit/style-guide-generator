import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from project.models.color_scheme_model import ColorScheme

os.environ['DATABASE_URL'] = "postgresql:///style_guide_maker_test"

from project import app, db