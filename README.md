# kami
The card game Kami implemented in Python

## Usage
`python main.py`

## Running Tests
`python -m unittest main.py`

## Bugs
- Empress can be played at any time
- Double points are not score when last two cards are duplicates
- Game is always played if a player is dealt 5 or more soldier cards
- Player starting each round is likely not accurrate with official rules

## Enhancement Goals
- Interchangeable AI
- AI that does not choose cards randomly
- 2 & 3 player variants
- Game end variants (Lord, Kami)
- Refactor code into classes
- Communicate nonblocking game events & actions between model / server and client
- Add human player(s) and CL interface for choosing cards and better seeing state of game
- Alternate GUI client
- Log and save game history when CL parameter is specified
- Automated tests
- Peer to peer network connection
- Deep learning integration

## Development Guidelines
- Use static typing where possible
- Variable and function name are in snake case
- Classes and types are in Pascal case
- Indent with tabs, align with spaces--tabs only appear at beginning of a line of code
- Two empty spaces between the declaration of types and functions
- Keep functions short and plenty

## Game Rules (per Board Game Arena)
https://en.doc.boardgamearena.com/Gamehelpkami
