import requests
import itertools
import sys
import time
from tags_extractor import extract

colors = [
        # White
        "\033[1;37m",
        # Green
        "\033[0;32m",
        # Blue
        "\033[0;34m",
        # Grey
        "\033[0;37m",
        # Yellow
        "\033[1;33m",
        # Orange
        "\033[38:5:208m",
        # Purple
        "\033[0;35m"
        ]


def main():
    try:
        operators = requests.get("https://rhodesapi.up.railway.app/api/operator").json()
    except requests.exceptions.ConnectionError:
        sys.exit("Request connection error")
    else:
        pass
    operators = prepare_operators(operators)

    try:
        while True:
            tags_from_screenshot = extract(currently_available_tags(operators))
            matching_cycle(tags_from_screenshot, operators)
            time.sleep(5)

    except KeyboardInterrupt:
        exit()


def matching_cycle(tags, operators):

    # Create combinations of all tags
    screenshot_combinations = tags_combinations(tags, 3)

    # Match tags combinations
    matched_operators = search_operators(screenshot_combinations, operators)

    # Sort matched operators by minimum rarity
    for combi in matched_operators:
        temp_rarity = 0
        for operator in combi["operators"]:
            # If combination have 3* operators or higher, making min_rarity 3* or higher
            # Since no one set recruitment time less than 8 hours (probably)
            if temp_rarity > 2 and operator["rarity"] > 2:
                if operator["rarity"] < temp_rarity:
                    temp_rarity = operator["rarity"]
            elif temp_rarity <= 2:
                temp_rarity = operator["rarity"]
        combi["min_rarity"] = temp_rarity
    matched_operators = sorted(matched_operators, key=lambda d: d["min_rarity"])

    # Temp output
    for combi in matched_operators:
        c = colors[combi["min_rarity"] - 1]
        print(f'{c}{combi["min_rarity"]} stars, {combi["combination"]}: ', end="")
        for operator in combi["operators"]:
            if not combi["min_rarity"] == 6 and operator["rarity"] == 6:
                continue
            c = colors[operator["rarity"] - 1]
            if operator["name"] == "Melantha":
                c = colors[6]
            print(f" {c}{operator['name']} {operator['rarity']}* |", end="")
        print()


def tags_combinations(tags, times):
    """
    Return list of all tags combinations
    """
    combination = []
    tmp = []
    for i in range(1, times + 1):
        tmp += list(itertools.combinations(tags, i))
    for combi in tmp:
        combination.append(set(combi))
    return combination


def search_operators(combinations, operators):

    """Returns list of tags combinations and operators that matches that tags"""

    matched_operators = []
    for combi in combinations:
        tmp = []
        temp_dict = {}
        for operator in operators:
            if combi in operator["combination"]:
                tmp.append(operator)
        if tmp:
            temp_dict["combination"] = combi
            temp_dict["operators"] = tmp
            matched_operators.append(temp_dict)

    return matched_operators


def currently_available_tags(operators: list):

    """Returns list of all available tags"""

    tags = []
    for operator in operators:
        for tag in operator["tags"]:
            if tag not in tags:
                tags.append(tag)
    return tags


def prepare_operators(operators: list):

    """
    Add positional and rarity tags to operators tag list
    Returns list with recruitable operators
    """

    ranged_classes = ["Medic", "Sniper", "Caster", "Decel Binder", "Bard", "Abjurer", "Summoner", "Tactician", "Hexer"]

    recruitable_operators = []

    for operator in operators:

        if operator["recruitable"] == "No":
            continue

        if operator["rarity"] == 6:
            operator["tags"].append("Top Operator")
        elif operator["rarity"] == 5:
            operator["tags"].append("Senior Operator")

        for class_name in operator["class"]:
            if class_name in ranged_classes:
                operator["tags"].append("Ranged")
                break
        else:
            operator["tags"].append("Melee")

        operator_combi = tags_combinations(operator["tags"], len(operator["tags"]))
        operator["combination"] = operator_combi

        recruitable_operators.append(operator)

    return recruitable_operators


if __name__ == "__main__":
    main()
