import sys
import os
import pytest

# Add the root directory to the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.main import play_location
from game.streamlit_app import examine_item, can_move_to, INIT_GAME_STATE, locations, items

@pytest.fixture
def game_state():
    return INIT_GAME_STATE.copy()

def test_examine_item(game_state):
    # Set game state
    game_state["current_location"] = "park"
    game_state["items_collected"] = []

    # Simulate Streamlit function
    def mock_write(message):
        print(message)

    # Replace Streamlit function with mock one
    st = type('obj', (object,), {'write': mock_write, 'session_state': {'game_state': game_state}})

    # Examine an existing object
    examine_item("tree")
    assert "map for square" in game_state["items_collected"]

    # Examine a non-existent object
    examine_item("nonexistent")
    assert "map for square" in game_state["items_collected"]

def test_can_move_to(game_state):
    # Set game state
    game_state["items_collected"] = ["map for square"]

    # Simulate Streamlit function
    def mock_write(message):
        print(message)

    # Replace Streamlit function with mock one
    st = type('obj', (object,), {'write': mock_write, 'session_state': {'game_state': game_state}})

    # Try to move to an accessible location
    assert can_move_to("square") == True

    # Try to move to an inaccessible location
    assert can_move_to("beach") == False

def test_play_location(game_state):
    # Set game state
    game_state["current_location"] = "park"
    game_state["items_collected"] = []
    game_state["locations_visited"] = []
    game_state["start_time"] = 0
    game_state["game_over"] = False

    # Simulate Streamlit function
    def mock_write(message):
        print(message)

    # Replace Streamlit function with mock one
    st = type('obj', (object,), {'write': mock_write, 'session_state': {'game_state': game_state}})

    # Play in one location
    play_location("park")
    assert "park" in game_state["locations_visited"]

    # Try to play in an inaccessible location
    play_location("beach")
    assert "beach" not in game_state["locations_visited"]