from unittest import TestCase
from django.conf import settings


class SettingsTestCase(TestCase):
    def test_login_url(self):
        self.assertEqual(settings.LOGIN_URL, "player_login")

    def test_redirect_url(self):
        self.assertEqual(settings.LOGIN_REDIRECT_URL, "player_home")

    def test_logout_redirect_url(self):
        self.assertEqual(settings.LOGOUT_REDIRECT_URL, "tictactoe_welcome")
