from unittest import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from gameplay.models import Game, Move, BOARD_SIZE


class GameTestCase(TestCase):
    def test_get_absolute_url_returns_correct_url(self):
        game = Game()
        game.id = 1
        target = reverse("gameplay_detail", args=[game.id])

        self.assertEqual(game.get_absolute_url(), target)

    def test_is_users_move_confirms_users_move(self):
        user = User()
        game = Game()

        game.first_player = user
        game.status = "F"

        self.assertTrue(game.is_users_move(user))

    def test_is_users_move_stops_wrong_users_move(self):
        user1 = User()
        user2 = User()
        game = Game()

        game.first_player = user1
        game.second_player = user2
        game.status = "F"

        self.assertFalse(game.is_users_move(user2))

    def test_board_returns_2_dimensional_list(self):
        game = Game()
        board = game.board()

        self.assertTrue(type(board) == list)
        self.assertTrue(type(board[0]) == list)
        self.assertTrue(len(board) == BOARD_SIZE)
        self.assertTrue(len(board[0]) == BOARD_SIZE)

    def test_new_move_returns_move(self):
        game = Game()
        game.status = "F"

        self.assertTrue(isinstance(game.new_move(), Move))

    def test_new_move_prevents_move_in_completed_game(self):
        game = Game()
        game.status = "W"

        self.assertRaises(ValueError, lambda: game.new_move())


class MoveTestCase(TestCase):
    def test_move_equality(self):
        move1 = Move()
        move1.by_first_player = True

        move2 = Move()
        move2.by_first_player = True

        self.assertEqual(move1, move2)

    def test_move_inequality(self):
        move1 = Move()
        move1.by_first_player = True

        move2 = Move()
        move2.by_first_player = False

        self.assertNotEqual(move1, move2)
