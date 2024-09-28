import streamlit as st
import time

# Definir ubicaciones y objetos
locations = {
    "park": {"name": "park", "description": "You are in a park with many trees and a playground.", "items": ["tree", "swing", "bench"], "exits": ["square"]},
    "square": {"name": "square", "description": "You are in a square with a fountain.", "items": ["bank", "fountain"], "exits": ["beach"]},
    "beach": {"name": "beach", "description": "You are on a beach with golden sand.", "items": ["towel", "umbrella", "seashell"], "exits": ["port"]},
    "port": {"name": "port", "description": "You are at the port. You can see the ferry.", "items": ["ticket office", "boat"], "exits": ["ferry"]},
    "ferry": {"name": "ferry", "description": "You are on the ferry. You have escaped the island!", "items": [], "exits": []}
}

items = {
    "tree": {"name": "map for square", "description": "A tall tree with a map hidden in it.", "type": "map"},
    "swing": {"name": "swing", "description": "A swing hanging from a tree.", "type": "object"},
    "bench": {"name": "bench", "description": "A bench to sit on.", "type": "object"},
    "bank": {"name": "map for beach", "description": "A bench with a map hidden under it.", "type": "map"},
    "fountain": {"name": "fountain", "description": "A beautiful fountain.", "type": "object"},
    "towel": {"name": "map for port", "description": "A towel with a map hidden under it.", "type": "map"},
    "umbrella": {"name": "umbrella", "description": "An umbrella providing shade.", "type": "object"},
    "seashell": {"name": "seashell", "description": "A beautiful seashell.", "type": "object"},
    "ticket office": {"name": "map for ferry", "description": "A ticket office with a map hidden in it.", "type": "map"},
    "boat": {"name": "boat", "description": "A small boat.", "type": "object"}
}

# Definir estado del juego
INIT_GAME_STATE = {
    "current_location": "park",
    "items_collected": [],
    "locations_visited": [],
    "start_time": time.time(),
    "end_time": None,
    "game_over": False
}

# Inicializar el estado del juego en la sesión
if "game_state" not in st.session_state:
    st.session_state["game_state"] = INIT_GAME_STATE.copy()
if "game_started" not in st.session_state:
    st.session_state["game_started"] = False

def start_game():
    st.session_state["game_state"] = INIT_GAME_STATE.copy()
    st.session_state["game_started"] = True
    st.write("You have woken up on an unknown island. Your goal is to find the ferry and escape the island. Good luck!")
    play_location(st.session_state["game_state"]["current_location"])

def play_location(location):
    if st.session_state["game_state"]["game_over"]:
        return

    current_time = time.time()
    elapsed_time = current_time - st.session_state["game_state"]["start_time"]
    remaining_time = 300 - elapsed_time

    if remaining_time <= 0:
        st.session_state["game_state"]["game_over"] = True
        st.write("Time's up! You lost.")
        show_summary()
        return

    st.write(f"Remaining time: {int(remaining_time)} seconds")

    st.session_state["game_state"]["current_location"] = location
    if location not in st.session_state["game_state"]["locations_visited"]:
        st.session_state["game_state"]["locations_visited"].append(location)

    if location == "ferry":
        st.session_state["game_state"]["end_time"] = current_time
        st.session_state["game_state"]["game_over"] = True
        st.write("Congratulations! You reached the ferry and escaped!")
        show_summary()
    else:
        loc = locations[location]
        st.write(loc["description"])
        intended_action = st.radio("What would you like to do?", ('Explore', 'Examine', 'Move'), key=f"radio_{location}_{len(st.session_state['game_state']['items_collected'])}")
        if intended_action == 'Explore':
            explore_location(location)
        elif intended_action == 'Examine':
            examine_item(st.text_input("What would you like to examine?", key=f"text_input_{location}_{len(st.session_state['game_state']['items_collected'])}").strip().lower())
        elif intended_action == 'Move':
            move_to = st.selectbox("Where would you like to go?", loc["exits"], key=f"move_{location}_{len(st.session_state['game_state']['items_collected'])}")
            if st.button("Go", key=f"go_{location}_{move_to}"):
                if can_move_to(move_to):
                    play_location(move_to)
                else:
                    st.write("You need to find the map to move to this location.")

def explore_location(location):
    items_in_location = locations[location]["items"]
    st.write(f"Items you can see: {', '.join(items_in_location)}")

def examine_item(item_name):
    current_location = st.session_state["game_state"]["current_location"]
    items_in_location = locations[current_location]["items"]
    if item_name in items_in_location:
        item = items[item_name]
        st.write(f"You examine the {item['name']}. {item['description']}")
        if item["type"] == "map":
            st.session_state["game_state"]["items_collected"].append(item["name"])
            st.write(f"You have collected the {item['name']}!")
    else:
        st.write("There is no such item here.")

def can_move_to(target_location):
    required_map = f"map for {target_location}"
    if required_map in st.session_state["game_state"]["items_collected"]:
        return True
    else:
        st.write(f"You need the {required_map} to move to {target_location}.")
        return False

def show_summary():
    st.write("Game Summary:")
    st.write(f"Locations visited: {', '.join(st.session_state['game_state']['locations_visited'])}")
    st.write(f"Items collected: {', '.join(st.session_state['game_state']['items_collected'])}")
    st.write(f"Total time: {int(st.session_state['game_state']['end_time'] - st.session_state['game_state']['start_time'])} seconds")

st.title("Adventure Game")
st.write("Welcome to the game")

if not st.session_state["game_started"]:
    if st.button("Come on!"):
        start_game()
else:
    play_location(st.session_state["game_state"]["current_location"])