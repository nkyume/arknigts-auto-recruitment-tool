import requests
import itertools
from tags_extractor import extract


def main():
    operators = requests.get("https://rhodesapi.up.railway.app/api/operator").json()
    tags_from_screenshot = extract(currently_available_tags(operators))
    operators = operator_sort(operators, tags_from_screenshot)

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
        combi["min_rarity"] = 6
        for operator in combi["operators"]:
            if operator["rarity"] < combi["min_rarity"]:
                combi["min_rarity"] = operator["rarity"]
    matched_operators = sorted(matched_operators, key=lambda d: d["min_rarity"], reverse=True)

    # Temp output
    for combi in matched_operators:
        print(f'{combi["min_rarity"]} stars, {combi["combination"]}: ', end="")
        for operator in combi["operators"]:
            if not combi["min_rarity"] == 6 and operator["rarity"] == 6:
                continue
            print(f" {operator['name']}", end="")
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


def operator_sort(operators: list, desired_tags: list):

    """
    Function that return list of operator's names and tags
    if their tags match with desired tags
    """

    matched_operators = []

    for operator in operators:
        temp_dict = {}
        temp_tag = set()

        if operator["recruitable"] == "No":
            continue

        for tag in desired_tags:
            if tag in operator["tags"]:

                temp_tag.add(tag)
                temp_dict["name"] = operator["name"]
                temp_dict["rarity"] = operator["rarity"]

                # Adding rarity tag since there no rarity tags on wiki page
                if operator["rarity"] == 6:
                    temp_tag.add("Top Operator")
                elif operator["rarity"] == 5:
                    temp_tag.add("Senior Operator")

        if temp_dict:
            temp_dict["tags"] = temp_tag
            matched_operators.append(temp_dict)

    return matched_operators


if __name__ == "__main__":
    main()
