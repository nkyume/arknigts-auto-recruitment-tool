import requests
from bs4 import BeautifulSoup
from time import sleep
import dbfunctions as db

def get_operators_data():
    url = "https://gamepress.gg/arknights/tools/interactive-operator-list"
    data = make_soup(url).find_all("tr", class_="operators-row")
    
    db.create_tables()
    missing_operators_id = get_missing_operators_id(data)
    
    missing = len(missing_operators_id)
    count = 0
    print(f"Found {missing} operators")
    for operator in data:
        
        if operator.get("data-id") in missing_operators_id:
            operator_urls = operator.find("div", class_="operator-icon")
            url_img = "https://gamepress.gg" + operator_urls.find("img").get("src")
            url_operator = "https://gamepress.gg" + operator_urls.find("a").get("href")
            
            operator_id = operator.get("data-id")
            operator_name = operator.get("data-name")
            operator_rarity = operator.get("data-rarity")
            operator_p_img = requests.get(url_img).content
            operator_tags = get_operator_tags(url_operator)
            
            if operator_rarity == "6":
                operator_tags.append("Top Operator")
            elif operator_rarity == "5":
                operator_tags.append("Senior Operator")
            
            db.add_to_db(operator_id, operator_name, operator_rarity,
                         operator_tags, operator_p_img)
            count += 1
            print(f"{operator_name} now in database![{count}/{missing}]")
            sleep(0.3)        

        
def get_operator_tags(url):
    
    data = make_soup(url)
    
    profession = data.find("div", class_="profession-title").text.strip()
    position = data.find("div", class_="position-cell")
    position = position.find("a").text.strip()
    raw_tags = data.find("div", class_="tag-cell").find_all("a")
    
    tags = [position, profession]
    
    for tag in raw_tags:
        tags.append(tag.text.strip())
          
    return tags


def make_soup(url):
    for i in range(5):
        try:
            response = requests.get(url)
        except requests.RequestException:
            print(f"Error occured {i}/5")
            sleep(5)
        else:
            break
    else:
        return
        
    return BeautifulSoup(response.text, "lxml")


def get_missing_operators_id(data):
    missing_operators = []
    for operator in data:
        id = operator.get("data-id")
        obtain_method = operator.find("div", class_="obtain-title").text
        
        if not db.exist_in_db(id) and "Recruitment" in obtain_method:
            missing_operators.append(id)
            
    return missing_operators
                

if __name__ == "__main__":
    get_operators_data()