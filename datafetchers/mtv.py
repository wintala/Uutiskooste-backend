import requests
import json

MTV_URL = "https://st.mtvuutiset.fi/data/linkpulse/1min.json"
VALID_FIELDS = ["url", "image", "title"]

def mtv_uutiset():
    res = requests.get(MTV_URL)

    if res.status_code != 200:
        raise Exception("Failed to fetch data")

    data_dict = json.loads(res.text)

    def filter_item(d):
        new_dict = {key: d["attributes"][key] for key in d["attributes"] if key in VALID_FIELDS}

        new_dict["url"] = "https://" + new_dict["url"]

        try:
            new_dict["picture"] = new_dict["image"]
            del new_dict["image"]
        except(KeyError):
            pass
        
        return new_dict
    
    return([filter_item(item) for item in data_dict["included"][:5]])
