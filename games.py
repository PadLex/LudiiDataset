import os
import re

class Game:
    def __init__(self, description: str):
        self.description = description
        self.name = re.search(r'game "(.+)"', description).group(1)

        self.option_groups = []
        for extract in find_ludemes(self.description, "option"):
            self.option_groups.append(parse_option(extract))

        self.local_definitions = []
        for extract in find_ludemes(self.description, "define"):
            self.local_definitions.append(extract)

    def get_game(self, selected_options: list):
        start = self.description.index("(game")
        end = closing_bracket(self.description, start)
        game_str = self.description[start:end].strip()

        for option in selected_options:
            for key, value in option.items():
                game_str = game_str.replace(key, value)

        return game_str.strip()

def parse_option(extract):
    groups = re.search(r'\(option(\s+)"(.+)"(\s+)<(.+)>(\s+)args:\{(.+)\}', extract).groups()
    groups = [groups for groups in groups if groups.strip()]
    name = groups[0]
    key = groups[1]
    print(groups[2])
    categories = re.findall(r'<(.+?)>', groups[2])

    item_extracts = find_ludemes(extract, "item")
    options = {}
    for item_extract in item_extracts:
        option = {}
        items = re.findall(r'<(.+?)>', item_extract)

        if len(items) != len(categories):
            raise Exception("Number of items and categories does not match")

        for item, category in zip(items, categories):
            option[f'<{key}:{category}>'] = item
        description = re.search(r'"([^"]*)"\s*\)\s*$', item_extract).group(1)
        options[description] = option

    return options


def find_ludemes(text: str, ludeme: str):
    sections = []
    while True:
        i = text.find('(' + ludeme + ' ', sections[-1][1] if sections else 0)
        if i == -1:
            break
        sections.append((i, closing_bracket(text, i)))

    extracts = []
    previous_end = -1
    for start, end in sections:
        if start > previous_end:
            extracts.append(text[start:end])

        previous_end = end

    return extracts


def closing_bracket(text, start):
    count = 0
    for i in range(start, len(text)):
        if text[i] == "(":
            count += 1
        elif text[i] == ")":
            count -= 1
        if count == 0:
            return i+1
    return -1


def get_games(game_dirs):
    games = []

    for game_dir in game_dirs:
        for dirpath, dirnames, filenames in os.walk(game_dir):
            for filename in filenames:
                if filename.endswith(".lud"):
                    with open(os.path.join(dirpath, filename), "r") as f:
                        games.append(Game(f.read()))

    return games

if __name__ == "__main__":
    with open("/Users/alex/Documents/Marble/Ludii/Common/res/lud/board/hunt/Hat Diviyan Keliya.lud", "r") as f:
        text = f.read()

        game = Game(text)
        print(game.name, '\n\n')
        for option_group in game.option_groups:
            print(option_group, '\n')

        print('\n\n', game.local_definitions, '\n\n')
        print(game.get_game([option_group[list(option_group.keys())[0]] for option_group in game.option_groups]))

        # for extract in find_ludemes(text, "option"):
        #     print(extract)
        #     print()