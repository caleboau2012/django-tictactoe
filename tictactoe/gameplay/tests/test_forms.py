from django.test import TestCase
from gameplay.forms import MoveForm
from gameplay.models import Game, Move
from django.core.exceptions import ValidationError


class MoveFormTestCase(TestCase):
    def setUp(self):
        game = Game()
        self.move = Move()
        self.move.game = game

    def test_valid_move(self):
        form_data = {"x": 0, "y": 1}
        form = MoveForm(data=form_data, instance=self.move)

        self.assertTrue(form.is_valid())

    def test_invalid_move(self):
        form_data = {"x": 5, "y": 7}
        form = MoveForm(data=form_data, instance=self.move)

        self.assertFalse(form.is_valid())
