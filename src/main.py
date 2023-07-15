import itertools
import sys
import time
import dbfunctions as db
from tags_extractor import extract
from scrapper import get_operators_data


def main():
    top_operator = False 
    tags = extract(db.available_tags(), "BlueStacks App Player")
    
    if "Top Operator" in tags:
        top_operator = True
    combinatons = tags_combinations(tags, 3)

    for combi in combinatons:
        tmp = "%".join(combi)
        operators = db.retrive_operators_by_tags(f"%{tmp}%")
        if operators:
            print(f"--{tmp.replace('%', ', ')}--")
            
            for operator in operators:
                if not top_operator and operator[1] == 6:
                    continue
                
                print(f"{operator[0]} {operator[1]}* | ", end="")
            print("\n")


def tags_combinations(tags, times):
    """
    Return list of all tags combinations
    """
    combination = []
    tmp = []
    for i in range(1, times + 1):
        tmp += itertools.combinations(tags, i)
    for combi in tmp:
        combination.append(sorted(list(combi)))
    return combination


if __name__ == "__main__":
    main()
    
