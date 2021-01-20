import requests
from bs4 import BeautifulSoup

YLE_URL = "https://yle.fi/uutiset"

def yle_uutiset():
    base_url = "https://yle.fi"
    res = requests.get(YLE_URL)

    if res.status_code != 200:
        raise Exception("Failed to fetch data")

    soup = BeautifulSoup(res.text, 'html.parser')

    list_html = soup.find(attrs={"data-test-key": "mostRead"}).find_all("li")

    def handle_item(item):
        return({"url": base_url + item.div.a["href"], 
                "picture": item.img["src"].replace("w_74", "w_600").replace("h_74", "h_338"), # jostain syystä muiden uutissivujen kuvien kuvasuhde tämä
                "title": item.div.a.div.h6.string
        })

    return [handle_item(item) for item in list_html]



