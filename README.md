# word-guessing-game

A simplified Hangman you play in the terminal. Pick a random secret word,
guess one letter at a time, and try to reveal the whole word before you run
out of wrong guesses.

Plain Python 3 — no third-party packages required.

## Files

| File | What it does |
| --- | --- |
| `game.py` | The game itself (entry point). |
| `state.py` | `GameState` — the secret word, guessed letters, wrong-guess count, win/lose checks. |
| `words.py` | Loads `data/words.txt` and picks a random secret word. |
| `test_state.py` | Unit tests for `GameState`. |
| `data/words.txt` | The word list — one word per line, `#` for comments. |

## Run it

```bash
python3 game.py
```

To see what the word list loader does on its own:

```bash
python3 words.py
```

Run the tests:

```bash
python3 -m unittest -v test_state.py
```

## Adding your own words

Open `data/words.txt` and add one lowercase word per line. Blank lines and
lines starting with `#` are skipped, and anything that isn't purely letters is
ignored, so you can annotate the file freely.

## Roadmap

- [x] Day 1 — Scaffold: README, `.gitignore`, word list + `load_words()` / `pick_word()`
- [x] Day 2 — Game state: secret word, guessed letters, wrong-guess count
- [ ] Day 3 — Guess loop with masked reveal and repeat-guess handling
- [ ] Day 4 — Wrong-guess limit plus win / lose endings
- [ ] Day 5 — Play again + simple score, README polish
