import requests
import itertools
from tags_extractor import extract


def main():
    operators = requests.get("https://rhodesapi.up.railway.app/api/operator").json()
    tags_from_screenshot = extract(currently_available_tags(operators))
    operators = operator_sort(operators)

    # Create combinations of all tags
    screen_combi = tags_combinations(tags_from_screenshot, 3)
    for operator in operators:
        operator_combi = tags_combinations(operator["tags"], len(operator["tags"]))
        operator["combination"] = operator_combi

    # Match tags combinations
    matched_operators = []
    for combi in screen_combi:
        tmp = []
        temp_dict = {}
        for operator in operators:
            if combi in operator["combination"]:
                tmp.append(operator)
        if tmp:
            temp_dict["combination"] = combi
            temp_dict["operators"] = tmp
            matched_operators.append(temp_dict)

    # Sort matched operators by minimum rarity
    for combi in matched_operators:
        temp_rarity = 0
        for operator in combi["operators"]:
            if temp_rarity > 2 and operator["rarity"] > 2:
                if operator["rarity"] < temp_rarity:
                    temp_rarity = operator["rarity"]
            elif temp_rarity <= 2:
                temp_rarity = operator["rarity"]
        combi["min_rarity"] = temp_rarity
    matched_operators = sorted(matched_operators, key=lambda d: d["min_rarity"])

    # Temp output
    for combi in matched_operators:
        print(f'{combi["min_rarity"]} stars, {combi["combination"]}: ', end="")
        for operator in combi["operators"]:
            if not combi["min_rarity"] == 6 and operator["rarity"] == 6:
                continue
            print(f" {operator['name']} {operator['rarity']}* |", end="")
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


def currently_available_tags(operators: list):
    tags = ["Top Operator", "Senior Operator", "Melee", "Ranged"]
    for operator in operators:
        for tag in operator["tags"]:
            if tag not in tags:
                tags.append(tag)
    return tags


def operator_sort(operators: list):

    """
    Function  add positional and rarity tags to operators tag list
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

        recruitable_operators.append(operator)

    return recruitable_operators


if __name__ == "__main__":
    main()
