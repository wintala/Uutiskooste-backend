import requests
from bs4 import BeautifulSoup
import json
import threading

IL_URL = "https://api.il.fi/v1/articles/iltalehti/lists/popular?limit=5&featured=coma-mostread&!fields[]=main_image_urls"
VALID_FIELDS = ["article_id", "category" , "title"]
IL_BASE_URL = "https://www.iltalehti.fi/"

def ilta_lehti():
    res = requests.get(IL_URL)

    if res.status_code != 200:
        raise Exception("Failed to fetch data")

    data_dict = json.loads(res.text)

    def filter_item(d):
        new_dict = {key: d[key] for key in d if key in VALID_FIELDS}

        new_dict["url"] = IL_BASE_URL + new_dict["category"]["category_name"] + "/a/" + new_dict["article_id"]
        del new_dict["category"]
        del new_dict["article_id"]
        
        return new_dict
    
    without_images = [filter_item(item) for item in data_dict["response"]]

    threads = []

    def add_image(article):
        res = requests.get(article["url"])
        soup = BeautifulSoup(res.text, 'html.parser')

        try:
            article["picture"] = soup.find("img", class_="image image-show")["src"]
        except(TypeError):
            pass


    for article in without_images:
        t = threading.Thread(target=add_image, args=[article])
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
        

    return(without_images)
