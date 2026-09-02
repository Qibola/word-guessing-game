"""Word guessing game (simplified Hangman).

Day 3 added the interactive guess loop. Day 4 closes the round out: the
wrong-guess limit is now visible (a gallows drawing plus a warning on the
last life) and the round ends with a proper win or lose message.
"""

from state import GameState
from words import pick_word


def show_status(state):
    """Print the board the player would see."""
    print(gallows_art(state.wrong_count, state.max_wrong))
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


# Seven stages, one per wrong guess when `max_wrong` is the default 6. Other
# limits are scaled onto these stages by `gallows_art()`.
GALLOWS = [
    "  +---+\n      |\n      |\n      |\n     ===",
    "  +---+\n  O   |\n      |\n      |\n     ===",
    "  +---+\n  O   |\n  |   |\n      |\n     ===",
    "  +---+\n  O   |\n /|   |\n      |\n     ===",
    "  +---+\n  O   |\n /|\\  |\n      |\n     ===",
    "  +---+\n  O   |\n /|\\  |\n /    |\n     ===",
    "  +---+\n  O   |\n /|\\  |\n / \\  |\n     ===",
]


def gallows_art(wrong_count, max_wrong):
    """The gallows drawing for this many wrong guesses.

    `max_wrong` can be any positive number: the wrong guesses are spread
    evenly over the available stages, so a 3-life game still starts empty
    and finishes with the full figure.
    """
    last = len(GALLOWS) - 1
    if max_wrong <= 0:
        return GALLOWS[last]
    stage = round(wrong_count * last / max_wrong)
    return GALLOWS[min(last, max(0, stage))]


def outcome(state):
    """Classify a round: "won", "lost", or "unfinished" (the player quit)."""
    if state.is_won:
        return "won"
    if state.is_lost:
        return "lost"
    return "unfinished"


def show_ending(state):
    """Print the closing message for a finished round.

    Returns the outcome string. A round the player walked away from gets no
    extra fanfare - `play_round()` has already revealed the word.
    """
    result = outcome(state)
    if result == "won":
        print(f"\nYou got it - the word was '{state.secret}'.")
        print(f"Solved with {state.wrong_count} wrong "
              f"{'guess' if state.wrong_count == 1 else 'guesses'} - "
              f"{state.guesses_left} of {state.max_wrong} lives unused.")
    elif result == "lost":
        print(gallows_art(state.wrong_count, state.max_wrong))
        print(f"\nOut of guesses - the word was '{state.secret}'.")
        print(f"You had it as {state.masked_word()}.")
    return result


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
            if state.guesses_left == 1:
                print("Careful - one wrong guess left.")
        else:  # repeat
            print(f"You already guessed '{guess}'. That one's free.")

        show_status(state)

    return state


def main():
    print("Word Guessing Game")
    print("------------------")
    state = play_round(GameState(pick_word()))
    show_ending(state)


if __name__ == "__main__":
    main()
