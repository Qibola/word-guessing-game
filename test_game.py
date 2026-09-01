"""Tests for the guess loop. Run with: python3 -m unittest -v test_game.py"""

import unittest

from game import play_round, read_guess
from state import GameState


def scripted_input(lines):
    """Fake `input()` that returns each line in turn, then raises EOFError."""
    it = iter(lines)

    def _input(_prompt=""):
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    return _input


class TestReadGuess(unittest.TestCase):
    def test_normalises_case_and_whitespace(self):
        self.assertEqual(read_guess(input_fn=scripted_input(["  B "])), "b")

    def test_reasks_until_a_single_letter_arrives(self):
        reader = scripted_input(["", "ab", "3", "q"])
        self.assertEqual(read_guess(input_fn=reader), "q")

    def test_returns_none_when_input_ends(self):
        self.assertIsNone(read_guess(input_fn=scripted_input([])))


class TestPlayRound(unittest.TestCase):
    def test_loop_ends_on_a_win(self):
        state = GameState("cat")
        play_round(state, input_fn=scripted_input(["c", "a", "t"]))
        self.assertTrue(state.is_won)
        self.assertEqual(state.masked_word(), "c a t")

    def test_loop_ends_when_guesses_run_out(self):
        state = GameState("cat", max_wrong=2)
        play_round(state, input_fn=scripted_input(["x", "y", "z"]))
        self.assertTrue(state.is_lost)
        self.assertEqual(state.wrong_count, 2)

    def test_repeat_guess_does_not_cost_a_life(self):
        state = GameState("cat", max_wrong=2)
        play_round(state, input_fn=scripted_input(["x", "x", "x"]))
        self.assertEqual(state.wrong_count, 1)
        self.assertFalse(state.is_over)

    def test_quitting_leaves_the_round_unfinished(self):
        state = GameState("cat")
        play_round(state, input_fn=scripted_input(["c"]))
        self.assertFalse(state.is_over)


if __name__ == "__main__":
    unittest.main()
