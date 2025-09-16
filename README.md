# cmput_657

Contains a CLI for the game clobber, and computer players (minimax, alpha- beta, and proof number). Proof Number Search works but currently runs until the game is solved. 
UPDATE: PNS may need some additional work to run correctly in the newly refactored code.

## Getting Started

There are a few dependencies that you'll need to install with pip. Just install a virtual environment (or don't, you crazy cat) and run:

```
pip install -r requirements.txt
```

Run the game from the command line by navigating to the project directory and typing:

```
python3 clobber.py
```

If you run the command "explain", the program will allow you to step through the first 50 steps of alpha-beta in the terminal. You can run "explain" on games of arbitrary size, but if the game is too large, you will just be shown the first 50 leaf nodes. I've found 3x3 games to be the most insightful. 

The point of "explain" is to provide a visual representation of alpha-beta search on a game of your choosing. To keep things running reasonably(-ish) efficiently, "explain" only goes 3 plies deep and uses a completely random heuristic. 

All algorithms in this repo are intended to explain, not to be efficient or high-functioning. Both minimax and proof number (when working) will find the best move, but there is no guarantee it will be quick.

The CLI recognizes the following commands:
- "help" (lists all acceptable commands)
- "quit" (exits the CLI)
- "size" (board size, e.g. "size 5x3")
- "play" (play a move, e.g. "play x b3 s" will move the piece x at position b3 south to capture the piece at b4)
- "show" (prints the current board)
- "ai {engine} {player}" (runs the specified search algorithm for player, e.g. "ai alphabeta x")
- "undo" (undoes the previous move)
- "explain {engine} {piece}": (plays a move using specified search algorithm to depth 3 (with randomized heuristic), then prints game tree step-by-step)

If you try to break the CLI, you will succeed. The checks to catch bad inputs are not robust. 

## Authors

Contributors names and contact info

Abel Romer  
[Website](https://ww.abelromer.com)
