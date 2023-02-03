# FROST 
A chess-like game with the following modifications: 
 - 10 by 10 playing board.
 - Knights will not move if they capture a piece.
 - Pawns are able to move sideways.
 - A "Deployment" phase before play begins.

---

# Setup
This project uses venv and pip in Python3.8 to manage packages. To setup and run the project, clone the repository and run the following commands in the root project directory:
1. `python3 -m venv ./`
2. `source bin/activate`
3. `python3 -m pip install -r requirements.txt`
4. Run `make` to start frost.

---

# Project Goals
 - [ ] Create a functioning one versus one game.
    - [x] Ability to move and capture pieces.
    - [x] Deployment and playing stages.
    - [ ] Preventing of illegal moves.
    - [ ] Castling, en passant, 50-move rule.
    - [ ] Determine a win/loss/tie.
 - [ ] Make an engine capable of beating novice human players.
