import re

class game:
    def __init__(self, description: str):
        self.description = description
        self.name = re.search(r'game "(.+)"', description).group(1)

    def get_game(self, option: dict):
        start = self.description.index("(game")
        end = closing_bracket(self.description, start)
        game_str = self.description[start:end].strip()

        for key, value in option.items():
            game_str = game_str.replace(key, value)

        return game_str


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

if __name__ == "__main__":
    with open("/Users/alex/Documents/Marble/Ludii/Common/res/lud/board/hunt/Hat Diviyan Keliya.lud", "r") as f:
        text = f.read()

        print(parse_option(text))

        # for extract in find_ludemes(text, "option"):
        #     print(extract)
        #     print()