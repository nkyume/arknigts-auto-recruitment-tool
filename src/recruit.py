import itertools
from time import sleep
import dbfunctions as db
from tags_extractor import extract
from scrapper import update_operators_data
import sys
import configparser 
import os

colors = {
        'white': '\033[1;37m',
        'green': '\033[38;5;28m',
        'blue': '\033[38;5;68m',
        'grey': '\033[38;5;240m',
        'yellow': '\033[38;5;226m',
        'orange': '\033[38;5;208m',
        'pink': '\033[38;5;218m',
        'purple': '\033[38;5;135m',
        'nocolor': '\33[0m'
        }

def main():
    try:
        if input('Update operators db? (y/n): ').lower() == 'y':
            update_operators_data()
        window_name, sleep_time = read_config_file()
        while True: 
            tags = extract(db.available_tags(), window_name)
            
            if not tags:
                continue
            
            cls()
            combinatons = combine_tags(tags, 3)
            avalible_operators = sorted(get_avalible_operators(combinatons), key=lambda d: d["combination_min_rarity"])
            
            # Console output
            for tag_combination in avalible_operators:
                tags_color = color_set(tag_combination['combination_min_rarity'])
                print(f"{tags_color}{tag_combination['combination_min_rarity']}* {tag_combination['combination']}{colors['nocolor']}: ", end="")
                
                for operator in tag_combination['operators']:
                    if operator['name'] == 'Melantha':
                        operator_color = colors['purple']
                    else:
                        operator_color = color_set(operator['rarity'])
                    print(f"{operator_color}{operator['name']} {operator['rarity']}* {colors['nocolor']} | ", end="")    
                print('\n', '-'*20)    
            sleep(sleep_time)
            
    except KeyboardInterrupt:
        sys.exit()
        
         
def color_set(rarity):   
    color = None
    match rarity:
        case 1:
            color = colors['grey']
        case 2:
            color = colors['green']
        case 3:
            color = colors['blue']
        case 4:
            color = colors['pink']
        case 5:
            color = colors['yellow']
        case 6:
            color = colors['orange']
        case _:
            color = colors['nocolor']
    return color


def get_avalible_operators(combinatons):
    avalible_operators = []
    
    for combi in combinatons:
        
        combi = "%|".join(combi)
        
        operators_raw = db.retrieve_operators_by_tags(f"%|{combi}|%")
        combi = combi.replace('|', ' ').replace('%', '')
        if not operators_raw:
            continue
        
        operators = []
        raritys = []
        # Get rid of 6* operators if no top tag
        for operator in operators_raw:
            if operator[1] == 6 and not 'Top Operator' in combi:
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
            tmp_raritys = []
            for rarity in raritys:
                if not rarity < 3:
                    tmp_raritys.append(rarity)
            raritys = tmp_raritys
            min_rarity = min(raritys)
            
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


def read_config_file():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return config['Settings']['window_name'], int(config['Settings']['sleep_time'])


def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    
       
if __name__ == "__main__":
    main()
    
