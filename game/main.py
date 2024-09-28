# game/main.py

import sys
import os

# Add the root directory to the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.locations import INIT_GAME_STATE
from game.functions import start_game

def main():
    game_state = INIT_GAME_STATE.copy()
    start_game(game_state)

if __name__ == "__main__":
    main()

