import os
import re

class Game:
    def __init__(self, file_string: str):
        self.file_string = file_string
        self.file_clean = re.sub(r'//.*', '', file_string)  # Remove comments
        self.name = re.search(r'game "(.+)"', self.file_clean).group(1)

        self.option_groups = []
        extracts = find_ludemes(self.file_clean, "option")
        for extract in extracts:
            self.option_groups.append(parse_option(self.file_clean, extract))

        self.local_definitions = []
        for extract in find_ludemes(self.file_clean, "define"):
            self.local_definitions.append(extract)

        #print("\n\n\n\n\n++++++++++++\n", self.file_string, "\n+++++++++++")
        metadata = find_ludemes(self.file_string, "metadata")[0]
        self.description = ""
        description = re.search(r'\(description "(.+?)"', metadata, re.DOTALL)
        if description:
            self.description += description.group(1)

        rules = re.search(r'\(rules "(.+?)"', metadata, re.DOTALL)
        if rules:
            self.description += rules.group(1)

    def get_game(self, selected_options=None):
        start = self.file_clean.index("(game")
        end = closing_bracket(self.file_clean, start)
        game_str = self.file_clean[start:end].strip()

        if selected_options is None:
            selected_options = [group[0] for group in self.option_groups]

        for option in selected_options:
            for key, value in option["items"].items():
                game_str = game_str.replace(key, value)

        return game_str.strip()


def count_asterisks(original_text, extract):
    index = original_text.find(extract) + len(extract) + 1

    count = 0
    while index < len(original_text) and original_text[index] == '*':
        count += 1
        index += 1

    return count


def parse_option(file_clean, extract):
    groups = re.search(r'\(option\s+\"(.+)\"\s+<(.+)>\s+args:\s*\{(.+?)\}', extract, re.DOTALL).groups()
    groups = [groups for groups in groups if groups.strip()]
    name = groups[0]
    key = groups[1]
    categories = re.findall(r'<(.+?)>', groups[2], re.DOTALL)

    item_extracts = find_ludemes(extract, "item")
    #sorted(item_extracts, key=lambda extract: count_asterisks(file_clean, extract))

    options = []
    for item_extract in item_extracts:

        option = {
            "description": re.search(r'"([^"]*)"\s*\)\s*$', item_extract).group(1),
            "items": {}
        }

        pattern = r''
        for _ in categories:
            pattern += r'<(.*)>\**\s*'

        items = re.search(pattern, item_extract, re.DOTALL).groups()

        if len(items) != len(categories):
            raise Exception("Number of items and categories does not match")

        for item, category in zip(items, categories):
            option["items"][f'<{key}:{category}>'] = item.strip()

        options.append(option)

    return options


def find_ludemes(text: str, ludeme: str):
    sections = []
    while True:
        offset = sections[-1][1] if sections else 0
        match = re.search(r'\(' + ludeme + r'\s', text[offset:]) # Find next ludeme. Start search after previous ludeme.
        if not match:
            break
        i = match.start() + offset
        assert text[i] == "("
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
                #print(os.path.join(dirpath, filename))
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
        print(game.get_game([option_group[list(option_group.keys())[0]] for option_group in game.option_groups]), '\n\n')

        print(game.description)
        print(game.rules, '\n\n')

        # for extract in find_ludemes(text, "option"):
        #     print(extract)
        #     print()