from django.urls import reverse
from gameplay.models import Game, Move
from django.test import TransactionTestCase, Client


class GameplayTransactionTestCase(TransactionTestCase):
    fixtures = ["tictactoe/tests/fixtures.json"]

    def setUp(self):
        self.game = Game.objects.get(pk=1)
        self.client = Client()

    def test_fixtures_load(self):
        self.assertTrue(Game.objects.count() > 0)

    def test_game_status_updates_after_move(self):
        old_status = self.game.status

        move = self.game.new_move()
        move.x = 0
        move.y = 0
        move.save()

        self.assertNotEqual(move.game.status, old_status)

    def test_game_detail_get(self):
        url = reverse("gameplay_detail", kwargs={"id": self.game.id})
        self.client.force_login(self.game.first_player)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gameplay/game_detail.html")

    def test_game_detail_get_404_guard(self):
        url = reverse("gameplay_detail", kwargs={"id": 1000})
        self.client.force_login(self.game.first_player)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_make_move_get(self):
        url = reverse("gameplay_make_move", kwargs={"id": self.game.id})
        self.client.force_login(self.game.first_player)
        data = {"x": 0, "y": 0, "game": self.game}

        response = self.client.post(url, data)

        self.assertRedirects(
            response, reverse("gameplay_detail", kwargs={"id": self.game.id})
        )

    def test_make_move_permission_guard(self):
        url = reverse("gameplay_make_move", kwargs={"id": self.game.id})
        self.client.force_login(self.game.second_player)
        data = {"x": 0, "y": 0, "game": self.game}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 403)

    def test_make_move_404_guard(self):
        url = reverse("gameplay_make_move", kwargs={"id": 1000})
        self.client.force_login(self.game.first_player)
        data = {"x": 0, "y": 0, "game": self.game}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 404)
