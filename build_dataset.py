import random
import json

from base_definitions import get_base_definitions
from games import get_games

common_dir = "/Users/alex/Documents/Marble/Ludii/Common"
definition_dir = "/res/def"
games_dirs = ["/res/lud/board", "/res/lud/experimental", "/res/lud/math", "/res/lud/puzzle"]

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
            "instruction": "What does the following global Ludii definition do?",
            "input": base_definition["ludii_code"].replace(base_definition["name"], "Unnamed"),
            "output": base_definition["description"]})

    for base_definition in base_definitions[cutoff:]:
        dataset.append({
            "instruction": "Construct a global Ludii definition which fulfills the following requirements.",
            "input": base_definition["description"],
            "output": base_definition["ludii_code"]})


def game_questions(explain_game=0.2, generate_local_definitions=0.2):
    games = get_games([common_dir + game_dir for game_dir in games_dirs])
    random.shuffle(games)

    explain_game_cutoff = int(len(games) * explain_game)
    for game in games[:explain_game_cutoff]:
        options = [group[0] for group in game.option_groups]
        dataset.append({
            "instruction": "Describe the mechanics of the following Ludii game",
            "input": game.get_game(options),
            "output": game.description + " " + " ".join(map(lambda option: option["description"], options))})

    for game in games[explain_game_cutoff:]:
        options = [group[0] for group in game.option_groups]
        dataset.append({
            "instruction": "Construct a Ludii game based on the following description",
            "input": game.description + " " + " ".join(map(lambda option: option["description"], options)),
            "output": game.get_game(options)})


def game_definitions():
    games = get_games([common_dir + game_dir for game_dir in games_dirs])
    random.shuffle(games)

    for game in games:
        if len(game.local_definitions) > 1:
            dataset.append({
                "instruction": "Construct the local definitions for the following Ludii game.",
                "input": game.get_game(),
                "output": "\n".join(game.local_definitions)})


def game_options():
    games = get_games([common_dir + game_dir for game_dir in games_dirs])
    random.shuffle(games)

    for game in games:
        options_one = []
        options_two = []
        for option_group in game.option_groups:
            filtered_group = list(filter(lambda group: group["description"].strip(), option_group))
            if len(filtered_group) >= 3:
                options_one.append(filtered_group[1])
                options_two.append(filtered_group[2])

        changes_str = "\n".join([f'{change1["description"]} -> {change2["description"]}'
                                 for change1, change2 in zip(options_one, options_two)])

        if len(changes_str) > 0:
            dataset.append({
                "instruction": f"Modify the Ludii game according to the following option changes:\n{changes_str}",
                "input": game.get_game(options_one),
                "output": game.get_game(options_two)
            })



if __name__ == "__main__":
    base_definition_questions()
    game_questions()
    game_definitions()
    game_options()

    random.shuffle(dataset)

    with open("dataset.json", "w") as f:
        json.dump(dataset, f, indent=4)

