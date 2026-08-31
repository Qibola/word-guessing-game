"""The game's state: the secret word, which letters have been guessed, and
how many of those guesses were wrong.

Keeping state in one small class means the guess loop (Day 3) only has to
call `record_guess()` and read a few properties, instead of juggling loose
variables.
"""

MAX_WRONG = 6


class GameState:
    """Tracks a single round of the word guessing game."""

    def __init__(self, secret, max_wrong=MAX_WRONG):
        secret = secret.strip().lower()
        if not secret.isalpha():
            raise ValueError(f"Secret word must be letters only, got {secret!r}")
        self.secret = secret
        self.max_wrong = max_wrong
        self.guessed = set()          # every letter guessed, right or wrong
        self.wrong_guesses = set()    # just the ones not in the secret

    # --- reading the state -------------------------------------------------

    @property
    def wrong_count(self):
        """How many wrong guesses have been made so far."""
        return len(self.wrong_guesses)

    @property
    def guesses_left(self):
        """How many wrong guesses remain before the round is lost."""
        return self.max_wrong - self.wrong_count

    @property
    def is_won(self):
        """True once every letter of the secret has been guessed."""
        return set(self.secret) <= self.guessed

    @property
    def is_lost(self):
        """True once the wrong guesses run out."""
        return self.guesses_left <= 0

    @property
    def is_over(self):
        return self.is_won or self.is_lost

    def masked_word(self):
        """The secret with unguessed letters hidden, e.g. 'c _ t'."""
        return " ".join(c if c in self.guessed else "_" for c in self.secret)

    # --- changing the state ------------------------------------------------

    def record_guess(self, letter):
        """Record one guessed letter.

        Returns one of: "hit", "miss", or "repeat" so the caller can decide
        what to print. A repeat never costs a guess.
        """
        letter = letter.strip().lower()
        if len(letter) != 1 or not letter.isalpha():
            raise ValueError(f"Guess must be a single letter, got {letter!r}")

        if letter in self.guessed:
            return "repeat"

        self.guessed.add(letter)
        if letter in self.secret:
            return "hit"
        self.wrong_guesses.add(letter)
        return "miss"

    def __repr__(self):
        return (
            f"GameState(secret={self.secret!r}, guessed={sorted(self.guessed)}, "
            f"wrong={self.wrong_count}/{self.max_wrong})"
        )
