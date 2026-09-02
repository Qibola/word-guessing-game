"""Tests for the guess loop. Run with: python3 -m unittest -v test_game.py"""

import unittest

from game import gallows_art, outcome, play_round, read_guess, show_ending
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


class TestGallowsArt(unittest.TestCase):
    def test_empty_at_the_start_and_full_at_the_limit(self):
        self.assertNotIn("O", gallows_art(0, 6))
        self.assertIn("O", gallows_art(6, 6))

    def test_scales_to_a_shorter_game(self):
        self.assertNotIn("O", gallows_art(0, 3))
        self.assertIn("O", gallows_art(3, 3))

    def test_never_indexes_past_the_last_stage(self):
        self.assertEqual(gallows_art(99, 6), gallows_art(6, 6))


class TestEndings(unittest.TestCase):
    def test_win_is_reported_as_won(self):
        state = GameState("cat")
        play_round(state, input_fn=scripted_input(["c", "a", "t"]))
        self.assertEqual(outcome(state), "won")
        self.assertEqual(show_ending(state), "won")

    def test_running_out_of_guesses_is_reported_as_lost(self):
        state = GameState("cat", max_wrong=2)
        play_round(state, input_fn=scripted_input(["x", "y"]))
        self.assertEqual(outcome(state), "lost")
        self.assertEqual(show_ending(state), "lost")

    def test_quitting_is_reported_as_unfinished(self):
        state = GameState("cat")
        play_round(state, input_fn=scripted_input(["c"]))
        self.assertEqual(show_ending(state), "unfinished")

    def test_a_win_on_the_last_life_still_counts_as_a_win(self):
        state = GameState("cat", max_wrong=2)
        play_round(state, input_fn=scripted_input(["x", "c", "a", "t"]))
        self.assertEqual(outcome(state), "won")
        self.assertEqual(state.guesses_left, 1)


if __name__ == "__main__":
    unittest.main()
