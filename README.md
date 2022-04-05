# ai-code
AI writes Python code. Or tries to.

This program uses an AI I wrote to generate a Python program, then removes errors from the program.

## How to run

1. To create an AI-generated Python file, run `python3 create.py`. This will generate the file `orig.py`.
2. To repeatedly run the generated program, removing all errors, run `python3 run.py`. The finished file will be stored in `done.py`.

### Generating program

`create.py` creates a Markov chain that I wrote. It is not very good at writing code because it guesses each new character based on _just the previous one_, i.e. a ONE CHARACTER MEMORY. The code is available in `markov.py`.

### Deleting errors

`run.py` repeatedly runs `orig.py`, and scans STDERR for `line` to find out what line the error was on. Then it removes that line from the program and repeats until it can't find an error in STDERR.

### Word mode

Normally, the AI is so bad at writing Python code, that the only thing left after deleting errors is comments and blank lines. However, you can turn on _word mode_ so the Markov chain guesses each new _word_ instead of each new _character_. To turn on word mode, run `WORD=y python3 create.py` instead of `python3 create.py`. The resulting text (you can look at the generated text in `orig.py`) is much more coherent than when running the Markov chain in character mode.

When generating text in word mode, and then running the program through `run.py`, you tend to get functions left in the resulting code.

## Interactive mode

There is a seperate feature called interactive mode. To start interactive mode, run `python3 interactive.py`. Type something into the terminal to get the Markov chain started, and the Markov chain's suggestion will appear under your cursor. To accept the suggestion, press Tab. To type an actual tab into the terminal, use Shift-Tab. If you don't like the suggestion, press Ctrl-Z. To exit interactive mode, press Ctrl-C. Arrow keys do not work.

Interactive mode is **much** better in word mode. To run it in word mode, use `WORD=y python3 interactive.py`. You will have to type a whole word into the terminal to get the Markov chain started (a good starting point is `# `), but after that, the resulting text is surprisingly coherent.

## Sources

Files to train the Markov chain on are located under `test_files`. `platformer.py` and `platformer_zombie.py` are from [my platformer game](https://github.com/sillypantscoder/pygame_platformer_2). `pygame_zip.py` is from [my pygame zip project](https://github.com/sillypantscoder/pygame_zip), and `towerdefense.py` is from my new project, a [tower defense game](https://github.com/sillypantscoder/pygametowerdefense).

A Javascript version of the Markov chain (doesn't support word mode!) is available at [https://ai.jasonroman.repl.co/markov/pkg.js](https://ai.jasonroman.repl.co/markov/pkg.js).