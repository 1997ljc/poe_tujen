import json

import requests

global league_name
league_name = "Affliction"

maps_url = f"https://poe.ninja/api/data/itemoverview?type=Map&league={league_name}"

data_json = requests.get(maps_url).json()['lines']
# 用于判断不同物品类型的URL

# if "itemoverview" in maps_url:
data_json = {x['icon']: x['chaosValue'] for x in data_json if x["name"] == "Waste Pool Map"}
# else:
#     data_json = {x['detailsId']: x['chaosEquivalent'] for x in data_json}


with open('./map.json', 'w') as file:
    json.dump(data_json, file, indent=4)