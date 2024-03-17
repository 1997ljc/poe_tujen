import json

import requests


def get_data(url):
    data_json = requests.get(url).json()['lines']
    # 用于判断不同物品类型的URL
    if "itemoverview" in url:
        data_json = {x['detailsId']: x['chaosValue'] for x in data_json}
    else:
        data_json = {x['detailsId']: x['chaosEquivalent'] for x in data_json}

    return data_json


if __name__ == "__main__":

    global league_name
    league_name = "Affliction"

    currency_url = f"https://poe.ninja/api/data/currencyoverview?league={league_name}&type=Currency"
    fossil_url = f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=Fossil"
    resonator_url = f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=Resonator"
    fragment_url = f"https://poe.ninja/api/data/currencyoverview?league={league_name}&type=Fragment"
    uniquemaps_url = f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=UniqueMap"
    scarabs_url = f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=Scarab"
    essences_url = f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=Essence"
    skillgem_url =f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=SkillGem"
    oils_url = f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=Oil"
    maps_url = f"https://poe.ninja/api/data/itemoverview?type=Map&league={league_name}"

# all these json are dir: "['detailsId']: ['chaosValue']"
    currency_json = get_data(currency_url)
    fossil_json = get_data(fossil_url)
    resonator_json = get_data(resonator_url)
    fragment_json = get_data(fragment_url)
# 再加一层字典
    all_json = {}
    all_json.update(currency_json)
    all_json.update(fossil_json)
    all_json.update(resonator_json)
    all_json.update(fragment_json)

    with open('./global_cprice.json', 'w') as file:
        json.dump(all_json, file, indent=4)



