import requests
import json

VALID_FIELDS = ["href", "picture", "title"]
IS_API_URL = "https://www.is.fi/api/laneitems/521057/list"
HS_API_URL = "https://www.hs.fi/api/laneitems/43949/list"
IS_BASE_URL = "https://www.is.fi"
HS_BASE_URL = "https://www.hs.fi"

def sanoma_api_handler(req_url, base_url):
    req = requests.get(req_url)
    if req.status_code != 200:
        raise Exception("Failed to fetch data")

    data_dict = json.loads(req.text)

    def filter_item(d):
        new_dict = {key: d[key] for key in d if key in VALID_FIELDS}
        new_dict["url"] = base_url + new_dict["href"]
        del new_dict["href"]

        try:
            new_dict["picture"] = new_dict["picture"]["url"].replace("WIDTH", "978")
        except(KeyError):
            pass
        
        return new_dict

    return([filter_item(item) for item in data_dict[:5]])

def ilta_sanomat():
    return sanoma_api_handler(IS_API_URL, IS_BASE_URL)

def helsingin_sanomat():
    return sanoma_api_handler(HS_API_URL, HS_BASE_URL)
