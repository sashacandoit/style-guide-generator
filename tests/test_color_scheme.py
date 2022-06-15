import unittest
from tests import BaseTestCase
from project.models.color_scheme_model import db, ColorScheme


COLOR_SCHEME_DATA = dict(
                    primary="000000",
                    secondary="ffffff",
                    accent_1="red",
                    accent_2="blue",
                    accent_3="green"
                )

class ColorSchemeModelTestCase(BaseTestCase):
    """Ensure model works properly"""

    # Can a new color scheme be added to the database
    def test_color_scheme_model(self):
        cs = ColorScheme(**COLOR_SCHEME_DATA)

        db.session.add(cs)
        db.session.commit()

        self.assertEqual(repr(cs), f"<ColorScheme {cs.user.username}-{cs.id}: Primary={cs.primary}, Secondary={cs.secondary}, Accent_1={cs.accent_1}, Accent_2={cs.accent_2}, Accent_3={cs.accent_3}>")