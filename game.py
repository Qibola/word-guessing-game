"""Word guessing game (simplified Hangman).

Day 2 adds the game state. This entry point sets up a round and shows what
the state object knows; the interactive guess loop arrives on Day 3 — see the
Roadmap in README.md.
"""

from state import GameState
from words import pick_word


def show_status(state):
    """Print the board the player would see."""
    print(f"Word:  {state.masked_word()}")
    print(f"Wrong: {state.wrong_count}/{state.max_wrong} "
          f"({state.guesses_left} left)")
    if state.wrong_guesses:
        print(f"Misses: {', '.join(sorted(state.wrong_guesses))}")


def main():
    state = GameState(pick_word())
    print("Word Guessing Game")
    print("------------------")
    print(f"The word has {len(state.secret)} letters.")
    show_status(state)
    print("\nThe interactive guess loop lands on Day 3.")


if __name__ == "__main__":
    main()
