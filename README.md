# word-guessing-game

A simplified Hangman you play in the terminal. The game picks a random secret
word, you guess one letter at a time, and you try to reveal the whole word
before you run out of wrong guesses. Win or lose, it asks whether you want
another round and keeps score for the session.

Plain Python 3 — no third-party packages required.

## Files

| File | What it does |
| --- | --- |
| `game.py` | The game itself: the guess loop, the play-again session, scoring, and the entry point. |
| `state.py` | `GameState` — the secret word, guessed letters, wrong-guess count, win/lose checks. |
| `words.py` | Loads `data/words.txt` and picks a random secret word. |
| `test_state.py` | Unit tests for `GameState`. |
| `test_game.py` | Unit tests for the guess loop, scoring and the session (scripted input, no typing). |
| `data/words.txt` | The word list — one word per line, `#` for comments. |

## Run it

```bash
python3 game.py
```

You'll be asked for one letter at a time. Repeat guesses are free, junk input
just gets re-asked, and Ctrl-D (or Ctrl-C) gives up and reveals the word.

Six wrong guesses end the round. The gallows drawing fills in as you miss,
you get a warning on your last life, and the round closes with a win or lose
message.

After each round you're asked `Play again? [y/n]`. Answer `y` for another
word; anything else (including Ctrl-D) ends the session and prints the
scoreboard.

## Scoring

Only wins score. A win is worth:

```
1 point per distinct letter in the word  +  2 points per unused life
```

So solving `cat` with no misses is `3 + 2×6 = 15` points, and solving it after
one miss is `3 + 2×5 = 13`. Losing or quitting a round scores nothing, which
makes guessing efficiently worth more than working through the alphabet.

The session ends with a recap:

```
Thanks for playing.
Rounds:  2
Won:     2
Lost:    0
Points:  28
```

To see what the word list loader does on its own:

```bash
python3 words.py
```

Run the tests:

```bash
python3 -m unittest -v test_state.py test_game.py
```

## Adding your own words

Open `data/words.txt` and add one lowercase word per line. Blank lines and
lines starting with `#` are skipped, and anything that isn't purely letters is
ignored, so you can annotate the file freely.

## Roadmap

- [x] Day 1 — Scaffold: README, `.gitignore`, word list + `load_words()` / `pick_word()`
- [x] Day 2 — Game state: secret word, guessed letters, wrong-guess count
- [x] Day 3 — Guess loop with masked reveal and repeat-guess handling
- [x] Day 4 — Wrong-guess limit plus win / lose endings
- [x] Day 5 — Play again + simple score, README polish

All five steps are done — the project is complete.
