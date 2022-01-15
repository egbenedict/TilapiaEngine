# Tilapia Chess Engine

<img src="https://static.wikia.nocookie.net/animalcrossing/images/8/8a/Tilapia.jpg/revision/latest?cb=20200519030338" alt="drawing" width="650"/>

## Introduction

Tilapia is an open-source chess engine coded entirely in Python over the course of 10 days in January of 2022. Tilapia currently has an ELO of approximately 1900-2000. While not optimized for runtime efficiency, Tilapia is definitely a lot more readable than a magic bitboard based engine. However, its slower speeds mean that it searches at lower depths, at times resulting in uncharacteristic blunders. If using for another project, please credit source as per the license. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pygame (if planning to use the Tilapia GUI).
```bash
pip3 install pygame
```

## Usage

Tilapia offers two primary modes, Terminal and GUI, explained below:

### Terminal
```bash
python3 terminal.py
```
A complete chess engine program in the command line, Tilapia's Terminal mode offers 3 levels of difficulty to play against. On your turn, enter moves using 
numbers assigned to each legal move on screen.
![p1](https://i.imgur.com/VcDU8sD.png)
Tilapia will then automatically respond with its own move. Keep in mind that on harder difficulty Tilapia may take longer thinks. If at any point you wish to play a move that two pieces could play, such as Nd2 in the following picture, enter `h` to see a detailed list of moves. Each move is shown along with a number representing the square that the piece being moved originates from. Numbers correspond to squares as in the third picture below (apologies for the lack of fully correct notation).

<img src="https://i.imgur.com/LQi394K.png" alt="drawing" width="250"/>

![p3](https://i.imgur.com/0nJnx5T.png)
![p4](https://i.stack.imgur.com/PFAvF.png)

To quit the game, enter `q`.

### GUI
```bash
python3 gui.py
```
A more refined (and easier on the eyes) depiction of the game, Tilapia's GUI offers Player vs Player and Player vs CPU modes. After choosing game mode, color, and difficulty, the GUI launches in a popup pygame window. Featuring legal move highlighting and a complete move log, the GUI will probably be your preferred way of using Tilapia. GUI mode also gives the user the option of loading a custom position by FEN.

To play a move, simply click on a piece and then click on a valid square to move to. In both GUI mode and Terminal mode, all rules of chess are supported. Yes, even en passant (mindboggling, I know... might do PIPI in my pampers...). 

<img src="https://i.imgur.com/06Y4lxy.png" alt="drawing" width="650"/>

Checkmate, stalemate, and other draws will be automatically recognized, ending the game. To quit during the game, close the popup window. Unfortunately, at this point, draw offers and resignations are not supported.

If making a promotion move, a prompt will appear in the terminal asking you to specify the piece you wish to promote.

There is also currently no way to flip the board if you are playing black. This will be added in a future update.

## Features
- Negamax algorithm with alpha-beta pruning
- Unlimited quiescent search
- Custom evaluation function that takes into account:
  - Material
  - Piece placement
  - Bishop pairs
  - Pawn structure (backward, passed, & doubled pawns, pawn islands)
  - Mobility
  - Tempo
- MVV-LVA move ordering (Most Valuable Victim - Least Valuable Aggressor)
- Full Transposition Table with Zobrist Hashing
- Complete Syzygy 7-piece Tablebases (internet connection required)
- Lichess API Opening Book

## Features to Come (hopefully)
- King Safety Evaluation
- Add checking moves to quiescent search
- Killer Heuristic
- Null Move Heuristic
- Correct PGN Notation
- Timed Games
- Texel Tuned Parameters
- Flip Board Option


## Why Tilapia?
I think every good chess engine should be named after a fish.

## Acknowledgements
- Chess Programming Wiki was a major resource
- My GUI is essentially a copy of Eddie Sharick's GUI in his Python chess engine Youtube series

## License
[GPL GNU v3](https://www.gnu.org/licenses/gpl-3.0.en.html)

