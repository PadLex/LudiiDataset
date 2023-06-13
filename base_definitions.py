import os
import re

def get_base_definitions(definition_dir):
    base_definitions = []

    for dirpath, dirnames, filenames in os.walk(definition_dir):
        for filename in filenames:
            if filename.endswith(".def"):
                with open(os.path.join(dirpath, filename), "r") as f:
                    base_definitions.append(parse_definition(f.read()))

    return base_definitions


def parse_definition(content):
    print(content)
    name = re.search(r'define "(.+)"', content).group(1)
    description = re.search(r'// (.+)', content).group(1)
    parameters_descriptions = re.findall(r'// #\d+ = (.+)', content)
    examples = re.findall(r'// @example (.+)\n', content)
    # Filter obvious examples
    examples = [example for example in examples if example != f'("{name}")']

    ludii_code = content[content.index("(define"):].strip()

    #anonymized_code = ludii_code.replace(name, "Anonymous")

    return {
        'name': name,
        'description': description,
        'parameters_descriptions': parameters_descriptions,
        'examples': examples,
        'ludii_code': ludii_code
    }


if __name__ == "__main__":
    for definition in get_base_definitions():
        print(definition)
        print()