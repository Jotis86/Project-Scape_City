import sys
import os
import pytest

# Añadir el directorio raíz al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.main import play_location
from game.streamlit_app import examine_item, can_move_to, INIT_GAME_STATE, locations, items

@pytest.fixture
def game_state():
    return INIT_GAME_STATE.copy()

def test_examine_item(game_state):
    # Configurar el estado del juego
    game_state["current_location"] = "park"
    game_state["items_collected"] = []

    # Simular la función de Streamlit
    def mock_write(message):
        print(message)

    # Reemplazar la función de Streamlit con la simulada
    st = type('obj', (object,), {'write': mock_write, 'session_state': {'game_state': game_state}})

    # Examinar un objeto existente
    examine_item("tree")
    assert "map for square" in game_state["items_collected"]

    # Examinar un objeto inexistente
    examine_item("nonexistent")
    assert "map for square" in game_state["items_collected"]

def test_can_move_to(game_state):
    # Configurar el estado del juego
    game_state["items_collected"] = ["map for square"]

    # Simular la función de Streamlit
    def mock_write(message):
        print(message)

    # Reemplazar la función de Streamlit con la simulada
    st = type('obj', (object,), {'write': mock_write, 'session_state': {'game_state': game_state}})

    # Intentar moverse a una ubicación accesible
    assert can_move_to("square") == True

    # Intentar moverse a una ubicación inaccesible
    assert can_move_to("beach") == False

def test_play_location(game_state):
    # Configurar el estado del juego
    game_state["current_location"] = "park"
    game_state["items_collected"] = []
    game_state["locations_visited"] = []
    game_state["start_time"] = 0
    game_state["game_over"] = False

    # Simular la función de Streamlit
    def mock_write(message):
        print(message)

    # Reemplazar la función de Streamlit con la simulada
    st = type('obj', (object,), {'write': mock_write, 'session_state': {'game_state': game_state}})

    # Jugar en una ubicación
    play_location("park")
    assert "park" in game_state["locations_visited"]

    # Intentar jugar en una ubicación inaccesible
    play_location("beach")
    assert "beach" not in game_state["locations_visited"]