# game/locations.py

# Define locations and items

ticket_office = {
    "name": "ticket office",
    "type": "object"
}

dog = {
    "name": "dog",
    "type": "object"
}

seagull = {
    "name": "seagull",
    "type": "object"
}

towel = {
    "name": "towel",
    "type": "object",
}

tree = {
    "name": "tree",
    "type": "object"
}

bank = {
    "name": "bank",
    "type": "object",
}

swing = {
    "name": "swing",
    "type": "object",
}

umbrella = {
    "name": "umbrella",
    "type": "object",
}

street_a = {
    "name": "street a",
    "type": "street",
}

street_b = {
    "name": "street b",
    "type": "street",
}

street_c = {
    "name": "street c",
    "type": "street",
}

street_d = {
    "name": "street d",
    "type": "street",
}

map_a = {
    "name": "map for street a",
    "type": "map",
    "target": street_a,
}

map_b = {
    "name": "map for street b",
    "type": "map",
    "target": street_b,
}

map_c = {
    "name": "map for street c",
    "type": "map",
    "target": street_c,
}

map_d = {
    "name": "map for street d",
    "type": "map",
    "target": street_d,
}

park = {
    "name": "park",
    "type": "location",
}

square = {
    "name": "square",
    "type": "location",
}

beach = {
    "name": "beach",
    "type": "location",
}

port = {
    "name": "port",
    "type": "location",
}

ferry = {
    "name": "ferry"
}

all_places = [park, square, beach, port, ferry]

all_streets = [street_a, street_b, street_c, street_d]

# Define which items/rooms are related

object_relations = {
    "park": [tree, swing, dog, street_a],
    "square": [bank, street_a, street_b, street_c],
    "beach": [towel, umbrella, street_b],
    "port": [street_c, ticket_office, seagull, street_d],
    "tree": [map_a],
    "bank": [map_b],
    "towel": [map_c],
    "ticket office": [map_d],
    "street a": [park, square],
    "street b": [square, beach],
    "street c": [square, port],
    "street d": [port, ferry],
}

# Define game state. Do not directly change this dict.
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_location": park,
    "maps_collected": [],
    "target_location": ferry,
    "game_over": False,
    "start_time": None,
    "end_time": None
}