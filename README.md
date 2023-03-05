# Checkers Milestone 1: project-rukrainsky-kcorra-jaguirre3-sjdoepker
This repository contains a design and implementation for Checkers. The existing bugs and inefficiencies will be resolved by Milestone 3. 

- Robert Ukrainsky - Game Logic
- Kasey Corra - Bot
- Jaslin Aguirre - GUI
- Sam Doepker - TUI

## Changes to design since Milestone 1
- transferred almost all functionality in `Board` class to `Game` to make the game the center component of the user interfaces. 
- 

## Summary of changes we’ve made/missing functionality we’ve added since Milestone 2

## How we implemented the feedback from milestones 1 and 2

# Running the Game
For running the Game Logic, no libraries will need to be used.
In python3, to start a game of checkers in its initial state, run the following
commands.
```
import checkers
game = checkers.Game()
```
To move a piece.call the `move_piece` method. If the piece move involves jumping,
the function will automatically call 'jump piece.' Alternatively, the the `jump_piece` 
method can be called. Call these functions by running game.move_piece(old_pos,new_pos,team)
and game.jump_piece(old_pos,new_pos,team). Their arguments are defined in their 
respective doc strings.Note, these methods work for any kind of piece regardless 
of if it's king.


To find a list of spots a piece can go to at a specific location, run the 
`list_moves` method (to find all moves, run `all_team_moves()`). To check if a 
move is valid, run the `is_valid_move` method. To find which argmuents each 
function takes and what they mean, refer to the code written for them and their
doc strings.

The `__str__` method will return a visual representation of the board at each 
iteration of the game. A regular red piece is represennted by 'r' and a king red 
piece is represented by 'R'. A regular black piece is represented by 'b' and a
king black piece is represented by 'B'.

The classes are the following:
`Piece`, which represents a checkers piece, has a team atttribute and an 
`is_king` attribute
`Board`, which represents a board of an arbitrary size, and will be an 8 by 8 
for the checkers game
`Game`, which represents the game itself and uses piece objects as well as a  
`Board` object to represent the board the game is being played on

Note that team can either be `"Red"` or `"Black"`


# Running the GUI
To run the GUI, run this from the root of the repository
```
python src/gui.py
```
By default, this will begin a game where a human player plays against the smart
bot. As the human player is Black, they must move first. 

To select a piece to move, click the piece. Once it has been selected, it will be
highlighted in green and the possible moves it can make will be highlighted in
yellow. To make a move, click on one of the highlighted pieces. To deselect the
piece simply click anywhere that's not highlighted in yellow.

To play a game with two human players on the same computer, run
```
python src/gui.py --red-type human
```

To make two bots play a game, run
```
python src/gui.py --black-type <bot> --red-type <bot>
```
where ```<bot>``` is ``smart-bot`` or ``random-bot``. When making two bots play
against it each other it is necessary to move your mouse around the pygame
window, so that pygame can recognize an event occuring. Otherwise the bots
will appear to 'freeze' and not move. 

To modify the number of rows and pieces on the board, run
```
python src/gui.py --num-piece-rows <int>
```
where ``<int>`` is the number of rows of pieces the checkerboard will have. 
The default is set to ``int=3`` as in a classic checkers game.

# TUI

To run the TUI, run this from the root of the repository:
```
python3 src/tui.py
```
If this does not work, instead use:
```
python src/tui.py
```
    
Due to the size and layout of the board, it's recommended you run in a terminal
left or right-aligned, as it will appear taller than it is wide.

The TUI shows the current board state and asks the player for the location of
a piece to move with a text prompt. Rows are numbered 0 to width of the 
board - 1 from the top to bottom, and columns are numbered left to right in the
same way. There are indices showing the numbering of rows and columns on the 
left and bottom of the board to help. (note: the bottom indices do not appear
perfectly on boards of ``C > 4`` due to double-digit numbers- they will run off
the side)

Possible moves for the selected piece will be shown on the board with question
marks in the appropriate spaces. If you enter a move that is not valid for any
reason, you will be prompted to re-enter the move.

To modify the number of rows of pieces on the board, run
```
python3 src/tui.py --num-piece-rows <num>
```
where ``<num>`` is the number of rows of checkers pieces the board will have.
The default is ``num = 3`` (a standard checkerboard). This parameter must come 
before bot parameters when running the TUI.

To play against a bot, run
```
python3 src/tui.py --player2 <bot>
```
where ``<bot>`` is ``random-bot`` or ``smart-bot``.

To have two bots play each other, run
```
python3 src/tui.py --player1 <bot> --player2 <bot>
```
The TUI inserts an artifical delay between each bot's move so you can see the 
game more easily. You can modify this delay using the ``--bot-delay <seconds>``
parameter.

# Bots
The `bots.py` file includes two classes:
- `RandomBot`: A bot that will just choose a move at random. 
- `SmartBot`: A bot that will try to make a winning move if possible. If not such move is possible, it checks whether the opposing player would win by the bot making a certain move and, if so, it does not make that move. 
    - It then checks if any move would make a piece a king. If so, it selects that move. If there are multiple such moves, it makes the following selections considering only those moves. If there are no king moves, it makes the following selections considering the all moves that were evaluated when looking for king moves.
    - The bot then finds the move that would result in the most number of jumps, or captures. If there are multiple such moves, it makes the following selections considering only those moves. If there are no jumping moves, it makes the following selections considering all moves that were evaluated when looking for maximum jumps.
    - The bot then finds the move with an end column closest to the center of the board. If there are multiple such moves, it chooses one of these moves at random. If there are no such moves, it picks a move at random from the moves that were evaluated when looking for centermost jumps.

These two classes are used in the TUI and GUI, but you can also run `bot.py` to run 1000 simulated games where two bots play each other (defaulted to one smart and one random), and see the percentage of wins and ties. For example:
```
$ python3 src/bot.py
Bot 1 (smart) wins: 99.40%
Bot 2 (random) wins: 0.00%
Ties: 0.60%

$ python3 src/bot.py --player1 random
Bot 1 (random) wins: 12.00%
Bot 2 (random) wins: 11.40%
Ties: 76.60%
```
Note: the 1000 game simulation should take about 2 minutes to run. For a faster result, run `python3 src/bot.py -n 100` or the like.


# Running with stubs and mocks
Stub and mock implementations of the Game class are available in the mocks.py file.

The TUI and GUI both accept a `--mode <mode>` parameter, where `<mode>` is one of:
- `real`: Use the `Game`(default)
- `stub`: Use the `StubCheckerboard`
- `mock`: Use the `MockGame`