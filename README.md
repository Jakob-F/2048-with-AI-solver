# 2048 Game with AI Solver
Welcome to my Python implementation of the classic 2048 game! This repository includes a playable version of 2048 and an AI that can play the game for you.

### How to play
To start the game, run:
```bash
python 2048.py
```
Arrows can be used for manual play. 

Press "space" to activate the AI.

Note, that once the AI has been activated, manual play is deactivated until the game terminates.

### AI Algorithm
The AI algorithm is based on the Monte Carlo algorithm, and it works in the following way:
- For each turn, the algorithm tries each of the four directions ('up', 'down', 'left', 'right') as the first move.
- For each direction, it checks if the move is valid.
- If the move is valid, it simulates 40 games from that new state, where in each game it makes random moves until the game ends or a move limit (num < 20) is reached.
- It then computes the average score of these simulations, and the direction with the highest average score is chosen as the best move
