"""Word guessing game (simplified Hangman).

Day 4 finished a single round. Day 5 turns one round into a session: after
each round you are asked whether to play again, a small scoreboard adds up
wins, losses and points, and the session prints a summary on the way out.
"""

from state import GameState
from words import load_words, pick_word


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


# --- scoring and the play-again loop --------------------------------------

def score_for_round(state):
    """Points for one finished round.

    A win is worth one point per letter revealed, plus a bonus for every
    unused life - guessing efficiently is worth more than guessing the whole
    alphabet. A loss or a round the player quit scores nothing.
    """
    if not state.is_won:
        return 0
    return len(set(state.secret)) + 2 * state.guesses_left


class Scoreboard:
    """Running totals for a session of rounds."""

    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.quits = 0
        self.points = 0

    @property
    def rounds(self):
        return self.wins + self.losses + self.quits

    def record(self, state):
        """Add one finished round. Returns the points it earned."""
        result = outcome(state)
        if result == "won":
            self.wins += 1
        elif result == "lost":
            self.losses += 1
        else:
            self.quits += 1

        earned = score_for_round(state)
        self.points += earned
        return earned

    def summary(self):
        """A one-line-per-fact recap of the session."""
        if self.rounds == 0:
            return "No rounds played."
        lines = [
            f"Rounds:  {self.rounds}",
            f"Won:     {self.wins}",
            f"Lost:    {self.losses}",
        ]
        if self.quits:
            lines.append(f"Quit:    {self.quits}")
        lines.append(f"Points:  {self.points}")
        return "\n".join(lines)

    def __repr__(self):
        return (f"Scoreboard(wins={self.wins}, losses={self.losses}, "
                f"quits={self.quits}, points={self.points})")


def ask_play_again(prompt="Play again? [y/n] ", input_fn=input):
    """Ask whether to play another round.

    Accepts y/yes/n/no in any case, re-asks anything else, and treats the end
    of input (Ctrl-D / Ctrl-C) as "no".
    """
    while True:
        try:
            raw = input_fn(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            return False

        answer = raw.strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer y or n.")


def play_session(words=None, input_fn=input, rng=None):
    """Play rounds until the player stops, then report the scoreboard.

    Returns the `Scoreboard` so tests (and any future caller) can inspect the
    session without reading the printed output.
    """
    board = Scoreboard()
    round_number = 1

    while True:
        print(f"\n--- Round {round_number} ---")
        secret = pick_word(words) if rng is None else pick_word(words, rng=rng)
        state = play_round(GameState(secret), input_fn=input_fn)
        show_ending(state)

        earned = board.record(state)
        if earned:
            print(f"+{earned} points (total {board.points}).")

        if not ask_play_again(input_fn=input_fn):
            break
        round_number += 1

    print("\nThanks for playing.")
    print(board.summary())
    return board


def main():
    print("Word Guessing Game")
    print("------------------")
    play_session(load_words())


if __name__ == "__main__":
    main()
