import random

from base_definitions import get_base_definitions
#from games import get_games

common_dir = "/Users/alex/Documents/Marble/Ludii/Common"
definition_dir = "/res/def"
games_dirs = ["/lud/board", "/lud/experimental", "/lud/math", "/lud/puzzle"]

exclude_matches = False
shorten_spaces = True

max_imbalance = 5

dataset = []
def base_definition_questions(explain=0.2):
    base_definitions = get_base_definitions(common_dir + definition_dir)
    random.shuffle(base_definitions)

    cutoff = int(len(base_definitions) * explain)
    for base_definition in base_definitions[:cutoff]:
        dataset.append({
            "instruction": "What does the following Ludii definition do?",
            "input": base_definition["ludii_code"].replace(base_definition["name"], "Unnamed"),
            "output": base_definition["description"]})

    for base_definition in base_definitions[cutoff:]:
        dataset.append({
            "instruction": "Construct a Ludii definition which fulfills the following requirements.",
            "input": base_definition["description"],
            "output": base_definition["ludii_code"]})



