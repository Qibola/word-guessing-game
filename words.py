"""Loading and choosing the secret word for the guessing game."""

import random
from pathlib import Path

DEFAULT_WORD_FILE = Path(__file__).parent / "data" / "words.txt"


def load_words(path=DEFAULT_WORD_FILE):
    """Read the word list, skipping blank lines and '#' comments.

    Returns a list of lowercase words made only of letters.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Word list not found: {path}")

    words = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip().lower()
        if not line or line.startswith("#"):
            continue
        if not line.isalpha():
            continue
        words.append(line)

    if not words:
        raise ValueError(f"No usable words found in {path}")
    return words


def pick_word(words=None, rng=random):
    """Pick one random word from the list (loads the default list if needed)."""
    if words is None:
        words = load_words()
    return rng.choice(words)


if __name__ == "__main__":
    all_words = load_words()
    print(f"Loaded {len(all_words)} words.")
    print(f"Random pick: {pick_word(all_words)}")
