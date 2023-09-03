import requests
from bs4 import BeautifulSoup
import dbfunctions as db
from tqdm import tqdm

def update_operators_data():
    """
    Create database if not exist.
    Update database if there missing operators.
    """
    url = "https://gamepress.gg/arknights/tools/interactive-operator-list"
    data = make_soup(url).find_all("tr", class_="operators-row")
    
    db.create_tables()
    missing_operators_id = get_missing_operators_id(data)
    
    #missing = len(missing_operators_id)
    
    # Count operators to look cool.
    count = 0
    #print(f"Found {missing} potentialy operators")
    
    for operator in tqdm(data, unit='operator'):
    
        if operator.get("data-id") in missing_operators_id:
            
            operator_urls = operator.find("div", class_="operator-icon")
            if operator_urls == None:
                continue
            url_operator = "https://gamepress.gg" + operator_urls.find("a").get("href")
            operator_tags = get_operator_tags(url_operator)
            

            # Part for checking if operator is recruitable
            if not operator_tags:
                continue
            operator_name = operator.get("data-name")
            url_img = "https://gamepress.gg" + operator_urls.find("img").get("src")
            operator_id = operator.get("data-id")
            operator_name = operator.get("data-name")
            operator_rarity = operator.get("data-rarity")
            operator_p_img = requests.get(url_img).content
            
            # Rarity tags.
            if operator_rarity == "6":
                operator_tags.append("Top Operator")
            elif operator_rarity == "5":
                operator_tags.append("Senior Operator")
            
            print()
            
            db.add_to_db(operator_id, operator_name, operator_rarity,
                         operator_tags, operator_p_img)
            count += 1
            # print(f"{operator_name} now in database![{count}/{missing}]")        

        
def get_operator_tags(url):
    """
    Return tags from operator page
    """
    data = make_soup(url)
    
    obtain_method = data.find(lambda tag: tag.name == "td" and "Recruitment:" in tag.text)
    obtain_method = obtain_method.find('span').text.strip()
    
    if obtain_method == 'No':
        return
    
    profession = data.find("div", class_="profession-title").text.strip()
    position = data.find("div", class_="position-cell")
    position = position.find("a").text.strip()
    raw_tags = data.find("div", class_="tag-cell").find_all("a")
    
    tags = [position, profession]
    
    for tag in raw_tags:
        tags.append(tag.text.strip())
    
    separated_tags = []
    for tag in tags:
        tag = tag_separate(tag)
        separated_tags.append(tag)
          
    return separated_tags

def tag_separate(tag):
    return f"|{tag}|"

def make_soup(url):
    for i in range(5):
        try:
            response = requests.get(url)
        except requests.RequestException:
            print(f"Error occured {i}/5")
        else:
            break
    else:
        return
        
    return BeautifulSoup(response.text, "lxml")


def get_missing_operators_id(data):
    missing_operators = []
    for operator in data:
        id = operator.get("data-id")
        obtain_method = operator.find("div", class_="obtain-title").text.strip()
        
        unwanted_obtain_methods = ["Event Reward", "Credit Store", "Voucher Exchange", "Main Story"]
        
        if not db.exist_in_db(id) and not obtain_method in unwanted_obtain_methods:
            missing_operators.append(id)
            
    return missing_operators