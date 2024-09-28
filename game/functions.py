# game/functions.py

import time
import threading
from game.locations import object_relations, INIT_GAME_STATE

def linebreak():
    """
    Print a line break.
    """
    print("\n\n")

def start_game(game_state):
    """
    Start the game. The player wakes up in a strange place and must escape.
    """
    game_state["start_time"] = time.time()
    print("You have woken up on an unknown island. You open your eyes and see that you are in a park. All around you you see many trees and a children's playground. Your only way out is to get to the harbour and catch the ferry...However, you don't know where the harbour is! You will have to look for the maps hidden in the different locations of the island and collect the lost maps to get out. Good luck!")
    start_timer(game_state)
    play_location(game_state, game_state["current_location"])

def start_timer(game_state):
    """
    Start a timer for 5 minutes. If the time runs out, the player loses the game.
    """
    def timer():
        time.sleep(300)  # 300 seconds = 5 minutes
        if not game_state["game_over"]:
            print("Time's up! You lost the game.")
            game_state["game_over"] = True
            game_state["end_time"] = time.time()
            final_report(game_state)

    timer_thread = threading.Thread(target=timer)
    timer_thread.start()

def play_location(game_state, location):
    """
    Play a location. Check if the location being played is the target location.
    If it is, the game ends with success. Otherwise, let the player explore or examine items.
    """
    if game_state["game_over"]:
        return
    game_state["current_location"] = location
    if game_state["current_location"] == game_state["target_location"]:
        print("Congrats! You reached the ferry and escaped!")
        game_state["game_over"] = True
        game_state["end_time"] = time.time()
        final_report(game_state)
    else:
        print(f"You are now in {location['name']}.")
        try:
            intended_action = input("What would you like to do? Type 'explore' or 'examine': ").strip().lower()
            if intended_action == "explore":
                explore_location(location)
                play_location(game_state, location)
            elif intended_action == "examine":
                examine_item(game_state, input("What would you like to examine? ").strip().lower())
            else:
                raise ValueError("Invalid action")
        except ValueError as e:
            print(f"Error: {e}. Please type 'explore' or 'examine'.")
            play_location(game_state, location)
        linebreak()

def explore_location(location):
    """
    Explore a location. List all items and streets belonging to this location.
    """
    items = [i["name"] for i in object_relations[location["name"]]]
    print(f"You explore the location. This is {location['name']}. You find: {', '.join(items)}")

def get_next_location_of_street(street, current_location):
    """
    From object_relations, find the two locations connected by the given street.
    Return the location that is not the current_location.
    """
    connected_locations = object_relations[street["name"]]
    for location in connected_locations:
        if not current_location == location:
            return location

def lost(game_state):
    """
    End the game if the player examines the dog or the seagull.
    """
    print("You lost the game")
    game_state["game_over"] = True
    game_state["end_time"] = time.time()
    final_report(game_state)

def examine_item(game_state, item_name):
    """
    Examine an item, which could be a street or furniture.
    Ensure the intended item belongs to the current location.
    If the item is a street, check if the required map has been collected.
    Otherwise, if the item is not a street, check if it contains a map.
    """
    current_location = game_state["current_location"]
    next_location = ""
    output = None

    # Find the item in the current location
    for item in object_relations[current_location["name"]]:
        if item["name"] == item_name:
            output = f"You examine {item_name}. "
            if (item["name"] == "dog" or item["name"] == "seagull"):
                lost(game_state)

            elif item["type"] == "street":
                have_map = False
                for map in game_state["maps_collected"]:
                    if map["target"] == item:
                        have_map = True
                if have_map:
                    output += "You unlock it with a map you have."
                    next_location = get_next_location_of_street(item, current_location)
                else:
                    output += "It is blocked. You don't have the map."
            else:
                # If the item is not a street, check if it contains a map
                if item["name"] in object_relations and len(object_relations[item["name"]]) > 0:
                    item_found = object_relations[item["name"]].pop()
                    game_state["maps_collected"].append(item_found)
                    output += f"You find {item_found['name']}."
                else:
                    output += "There isn't anything interesting about it."
            if (item["name"] != "dog" and item["name"] != "seagull"):
                print(output)
                break
            else:
                pass

    if output is None:
        print("The item you requested is not found in the current location.")

    if next_location and input("Do you want to go to the next location? Enter 'yes' or 'no': ").strip().lower() == 'yes':
        play_location(game_state, next_location)
    else:
        play_location(game_state, current_location)

def final_report(game_state):
    """
    Generate the final report including maps collected, time elapsed, time remaining, and moves made.
    """
    end_time = game_state["end_time"]
    start_time = game_state["start_time"]
    time_elapsed = round(end_time - start_time)
    time_remaining = max(0, 300 - time_elapsed)
    maps_collected = [map["name"] for map in game_state["maps_collected"]]
    moves_made = len(game_state["maps_collected"])  # Assuming each map collected is a move

    print("\nFinal Report")
    print("============")
    print(f"Maps collected: {', '.join(maps_collected)}")
    print(f"Time elapsed: {time_elapsed} seconds")
    print(f"Time remaining: {time_remaining} seconds")
    print(f"Moves made: {moves_made}")