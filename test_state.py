"""Tests for GameState. Run with: python3 -m unittest -v test_state.py"""

import unittest

from state import GameState


class TestGameState(unittest.TestCase):
    def test_starts_fully_masked(self):
        state = GameState("cat")
        self.assertEqual(state.masked_word(), "_ _ _")
        self.assertEqual(state.wrong_count, 0)
        self.assertFalse(state.is_over)

    def test_hit_reveals_every_copy_of_the_letter(self):
        state = GameState("banana")
        self.assertEqual(state.record_guess("a"), "hit")
        self.assertEqual(state.masked_word(), "_ a _ a _ a")
        self.assertEqual(state.wrong_count, 0)

    def test_miss_costs_a_guess(self):
        state = GameState("cat", max_wrong=3)
        self.assertEqual(state.record_guess("z"), "miss")
        self.assertEqual(state.wrong_count, 1)
        self.assertEqual(state.guesses_left, 2)

    def test_repeat_guess_is_free(self):
        state = GameState("cat")
        state.record_guess("z")
        self.assertEqual(state.record_guess("z"), "repeat")
        self.assertEqual(state.wrong_count, 1)
        state.record_guess("c")
        self.assertEqual(state.record_guess("c"), "repeat")

    def test_win_when_all_letters_guessed(self):
        state = GameState("cat")
        for letter in "cat":
            state.record_guess(letter)
        self.assertTrue(state.is_won)
        self.assertFalse(state.is_lost)
        self.assertTrue(state.is_over)

    def test_loss_when_guesses_run_out(self):
        state = GameState("cat", max_wrong=2)
        state.record_guess("x")
        state.record_guess("y")
        self.assertTrue(state.is_lost)
        self.assertFalse(state.is_won)

    def test_case_and_whitespace_are_normalised(self):
        state = GameState("  Cat \n")
        self.assertEqual(state.secret, "cat")
        self.assertEqual(state.record_guess(" A "), "hit")

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            GameState("cat!")
        with self.assertRaises(ValueError):
            GameState("cat").record_guess("ab")
        with self.assertRaises(ValueError):
            GameState("cat").record_guess("3")


if __name__ == "__main__":
    unittest.main()
