"""Word guessing game (simplified Hangman).

Day 1 is the scaffold: it loads the word list and shows the masked word.
The guessing loop arrives on Day 3 — see the Roadmap in README.md.
"""

from words import pick_word

MAX_WRONG = 6


def mask_word(secret, guessed):
    """Show the secret with unguessed letters hidden as underscores.

    >>> mask_word("cat", {"c"})
    'c _ _'
    """
    return " ".join(letter if letter in guessed else "_" for letter in secret)


def main():
    secret = pick_word()
    print("Word Guessing Game")
    print("------------------")
    print(f"The word has {len(secret)} letters: {mask_word(secret, set())}")
    print(f"You will get {MAX_WRONG} wrong guesses once the game loop is built.")


if __name__ == "__main__":
    main()
