from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User


class WelcomeViewTestCase(TestCase):
    def setUp(self):
        self.username = "user"
        self.password = "valid_password1"
        self.client = Client()
        self.url = reverse("tictactoe_welcome")

        User.objects.create_user(self.username, "email@test.com", self.password)

    def test_home_sends_user_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Let's play Tic Tac Toe")

    def test_home_redirects_user_to_player_home(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse("player_home"))

