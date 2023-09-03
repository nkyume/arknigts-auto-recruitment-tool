import itertools
from time import sleep
import dbfunctions as db
from tags_extractor import extract
from scrapper import update_operators_data


def main():
    if input('Update operators list? (y/n): ') == 'y':
        update_operators_data()
    
    while True:
        is_top_operator = False 
        tags = extract(db.available_tags(), "BlueStacks App Player")
        
        # Flag for Top Operator tag
        if "Top Operator" in tags:
            top_operator = True
            
        combinatons = combine_tags(tags, 3)
        avalible_operators = sorted(get_avalible_operators(combinatons, is_top_operator), key=lambda d: d["combination_min_rarity"])
        avalible_operators.reverse()
        
        for tag_combintaion in avalible_operators:
            print(tag_combintaion['combination'], tag_combintaion['combination_min_rarity'],)
        # Temp output
        """ for combi in combinatons:
            
            tmp = "%".join(combi)
            operators = db.retrieve_operators_by_tags(f"%{tmp}%")
            
            if operators:
                print(f"--{}--")
                
                for operator in operators:
                    if not top_operator and operator[1] == 6:
                        continue
                    
                    print(f"{operator[0]} {operator[1]}* | ", end="")
                print("\n")
         """
        sleep(5)


def get_avalible_operators(combinatons, is_top_operator):
    avalible_operators = []
    
    for combi in combinatons:
        
        combi = "%".join(combi)
        operators_raw = db.retrieve_operators_by_tags(f"%{combi}%")
        combi = combi.replace('%', ', ')
        if not operators_raw:
            continue
        operators = []
        min_rarity = 0
        raritys = []
        
        # Get rid of 6* operators if no top tag
        for operator in operators_raw:
            if operator[1] == 6 and not is_top_operator:
                continue
            
            tmp_operator = {
                'name': operator[0],
                'rarity': operator[1],
                'tags': operator[2],
                #'image': operator[3]    
            }
            operators.append(tmp_operator)
            raritys.append(tmp_operator["rarity"])
        if not raritys:
               continue
        if set(raritys) == {1}:
            min_rarity = 1
        elif set(raritys) == {2}:
            min_rarity = 2
        elif set(raritys) == {6}:
            min_rarity = 6
        else:
            min_rarity = min(raritys)
            if min_rarity < 3:
                min_rarity = 3

        tmp_tags = {
            'combination': combi,
            'combination_min_rarity': min_rarity,
            'operators': operators,   
        }    
          
        avalible_operators.append(tmp_tags)
    return avalible_operators    
                 
def combine_tags(tags, times):
    """
    Return combinations of all tags 
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
    
