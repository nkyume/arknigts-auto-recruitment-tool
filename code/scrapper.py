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
    missing_operators = get_missing_operators()
    
    # missing = len(missing_operators)
    
    # Count operators to look cool.
    # count = 0
    print(f"Found {len(missing_operators)} operators")
    
    for operator in tqdm(data, unit='operator'):
    
        if operator.get("data-name") in missing_operators:
            
            operator_urls = operator.find("div", class_="operator-icon")
            if operator_urls == None:
                continue
            url_operator = "https://gamepress.gg" + operator_urls.find("a").get("href")
            operator_tags = get_operator_tags(url_operator)

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
                operator_tags.append("|Top Operator|")
            elif operator_rarity == "5":
                operator_tags.append("|Senior Operator|")
            
            db.add_to_db(operator_id,
                        operator_name,
                        operator_rarity,
                        operator_tags,
                        operator_p_img)
            # count += 1
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
        tag = f"|{tag}|"
        separated_tags.append(tag)
     
    return separated_tags


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


def get_missing_operators():
    url = "https://gamepress.gg/arknights/database/operator-release-dates-and-how-obtain"
    data = make_soup(url).find("table", class_="views-table views-view-table cols-5").find('tbody')
    data = data.find_all("tr")
    operators = []

    for operator in data:
        name = operator.find("td", class_="views-field views-field-title").get_text().strip()
        obtain_method = operator.find("td", class_="views-field views-field-field-obtain-approach").get_text()
        if "Recruitment" in obtain_method and not db.exist_in_db(name):    
            operators.append(name)

    return operators

if __name__ = "__main__":
    update_operators_data()
        



