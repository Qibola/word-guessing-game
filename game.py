"""Word guessing game (simplified Hangman).

Day 3 adds the interactive guess loop: ask for a letter, validate it, hand it
to `GameState.record_guess()`, and redraw the masked word. The win / lose
endings arrive on Day 4 — see the Roadmap in README.md.
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


def read_guess(prompt="Guess a letter: ", input_fn=input):
    """Ask for a single letter, re-asking until the input is usable.

    Returns the lowercase letter, or None if the player gives up (Ctrl-D,
    Ctrl-C, or the end of piped input).
    """
    while True:
        try:
            raw = input_fn(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            return None

        guess = raw.strip().lower()
        if len(guess) == 1 and guess.isalpha():
            return guess
        if not guess:
            print("Type a letter first.")
        else:
            print(f"'{raw.strip()}' isn't a single letter - try again.")


def play_round(state, input_fn=input):
    """Run the guess loop until the round is over or the player quits.

    Returns the finished state so the caller can report the outcome.
    """
    print(f"The word has {len(state.secret)} letters.")
    show_status(state)

    while not state.is_over:
        print()
        guess = read_guess(input_fn=input_fn)
        if guess is None:
            print(f"Giving up - the word was '{state.secret}'.")
            return state

        result = state.record_guess(guess)
        if result == "hit":
            print(f"Yes - '{guess}' is in the word.")
        elif result == "miss":
            print(f"No - '{guess}' isn't in the word.")
        else:  # repeat
            print(f"You already guessed '{guess}'. That one's free.")

        show_status(state)

    return state


def main():
    print("Word Guessing Game")
    print("------------------")
    state = play_round(GameState(pick_word()))
    if state.is_over:
        print("\nRound over - win / lose messages land on Day 4.")


if __name__ == "__main__":
    main()
