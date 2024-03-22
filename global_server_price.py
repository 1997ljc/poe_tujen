import json
import os
import requests


def get_data(url):
    data_json = requests.get(url).json()['lines']
    # 用于判断不同物品类型的URL
    if "itemoverview" in url:
        data_json = {x['detailsId']: x['chaosValue'] for x in data_json}
    else:
        data_json = {x['detailsId']: x['chaosEquivalent'] for x in data_json}

    return data_json


def get_global_data(league_name):
    currency_url = f"https://poe.ninja/api/data/currencyoverview?league={league_name}&type=Currency"
    fossil_url = f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=Fossil"
    resonator_url = f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=Resonator"
    fragment_url = f"https://poe.ninja/api/data/currencyoverview?league={league_name}&type=Fragment"
    uniquemaps_url = f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=UniqueMap"
    scarabs_url = f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=Scarab"
    essences_url = f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=Essence"  # 精华只留咆哮往上的
    # skillgem_url =f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=SkillGem"
    oils_url = f"https://poe.ninja/api/data/itemoverview?league={league_name}&type=Oil"
    maps_url = f"https://poe.ninja/api/data/itemoverview?type=Map&league={league_name}"


    # all these json are dir: "['detailsId']: ['chaosValue']"
    currency_json = get_data(currency_url)
    fossil_json = get_data(fossil_url)
    resonator_json = get_data(resonator_url)
    fragment_json = get_data(fragment_url)
    scarabs_json = get_data(scarabs_url)
    essences_json = get_data(essences_url)
    uniquemaps_json = get_data(uniquemaps_url)
    maps_json = get_data(maps_url)
    oils_json = get_data(oils_url)
    # # 再加一层字典
    all_json = {}
    all_json.update(currency_json)
    all_json.update(fossil_json)
    all_json.update(resonator_json)
    all_json.update(fragment_json)
    all_json.update(scarabs_json)
    all_json.update(essences_json)
    all_json.update(uniquemaps_json)
    all_json.update(maps_json)
    all_json.update(oils_json)
    #
    # with open('./global_price.json', 'w') as file:
    #     json.dump(all_json, file, indent=4)

    chinese_english_alias_dir = {
        # 通货
        'awakened-sextant': '觉醒六分仪',
        'blessed-orb': '祝福石',
        'cartographers-chisel': '制图钉',
        'chromatic-orb': '幻色石',
        'divine-orb': '神圣石',
        'exalted-orb': '崇高石',
        'gemcutters-prism': '宝石匠的棱镜',
        'jewellers-orb': '工匠石',
        'orb-of-alchemy': '点金石',
        'orb-of-alteration': '改造石',
        'orb-of-binding': '高阶点金石',
        'orb-of-fusing': '链结石',
        'orb-of-regret': '后悔石',
        'orb-of-scouring': '重铸石',
        'regal-orb': '富豪石',
        'stacked-deck': '未知的命运卡',
        'vaal-orb': '瓦尔宝珠',
        'armourers-scrap': '护甲片',
        'blacksmiths-whetstone': '磨刀石',
        'orb-of-transmutation': '蜕变石',
        'orb-of-augmentation': '增幅石',
        'orb-of-chance': '机会石',
        'rogues-marker': '赏金猎人印记',
        'glassblowers-bauble':'玻璃弹珠',
        # 有碎片的
        'orb-of-annulment':'剥离石',
        'orb-of-horizons':'平行石',
        'harbingers-orb':'先驱石',
        # 化石
        'perfect-fossil': '完美化石',
        'shuddering-fossil': '震颤化石',
        'sanctified-fossil': '圣洁化石',
        'corroded-fossil': '腐蚀化石',
        'gilded-fossil': '镶金化石',
        'bound-fossil': '绑缚化石',
        'fundamental-fossil': '根基化石',
        'serrated-fossil': '狼牙化石',
        'deft-fossil': '机巧化石',
        'aetheric-fossil': '以太化石',
        'jagged-fossil': '锯齿化石',
        'aberrant-fossil': '畸变化石',
        'dense-fossil': '致密化石',
        'metallic-fossil': '金属化石',
        'prismatic-fossil': '五彩化石',
        'pristine-fossil': '原始化石',
        'scorched-fossil': '炽炎化石',
        'frigid-fossil': '冰冽化石',
        'lucent-fossil': '透光化石',
        'prime-chaotic-resonator': '威能混乱共振器',
        # 其他裂片
        'simulacrum': '梦魇拟像',
        'ritual-vessel': '驱灵法器',
        'timeless-maraketh-emblem': '永恒马拉克斯印记',
        'timeless-templar-emblem': '永恒圣堂印记',
        'timeless-vaal-emblem': '永恒瓦尔印记',
        'timeless-karui-emblem': '永恒卡鲁印记',
        'timeless-eternal-emblem': '永恒帝国印记',
        'uul-netols-breachstone': '乌尔尼多裂隙石',
        'xophs-breachstone': '索伏裂隙石',
        'eshs-breachstone': '艾许裂隙石',
        'tuls-breachstone': '托沃裂隙石',
        'chayulas-breachstone': '夏乌拉裂隙石',
        # 地图
        'cortex-t11': '脑层',
        'pit-of-the-chimera-map-t16-gen-19': '奇美拉领域',
        'maze-of-the-minotaur-map-t16-gen-19': '牛头人迷宫',
        'lair-of-the-hydra-map-t16-gen-19': '九头蛇巢穴',
        'forge-of-the-phoenix-map-t16-gen-19': '不死鸟锻台',
        # 地图碎片
        'sacrifice-at-midnight': '午夜的奉献',
        'sacrifice-at-dusk': '黄昏的奉献',
        'sacrifice-at-dawn': '黎明的奉献',
        'sacrifice-at-noon': '正午的奉献',
        'mortal-grief': '凡人的哀伤',
        'mortal-ignorance': '凡人的无知',
        'mortal-rage': '凡人的愤怒',
        'mortal-hope': '凡人的希望',
        # 圣油
        'amber-oil': '琥珀圣油',
        'azure-oil': '天蓝圣油',
        'black-oil': '漆黑圣油',
        'clear-oil': '清澈圣油',
        'crimson-oil': '绯红圣油',
        'golden-oil': '金色圣油',
        'opalescent-oil': '乳白圣油',
        'sepia-oil': '墨色圣油',
        'silver-oil': '白银圣油',
        'teal-oil': '水蓝圣油',
        'verdant-oil': '翠绿圣油',
        'violet-oil': '紫色圣油',

        # 精华
        'shrieking-essence-of-greed': '贪婪之咆哮精华',
        'shrieking-essence-of-contempt': '轻视之咆哮精华',
        'shrieking-essence-of-hatred': '憎恨之咆哮精华',
        'shrieking-essence-of-woe': '悲痛之咆哮精华',
        'shrieking-essence-of-fear': '恐惧之咆哮精华',
        'shrieking-essence-of-anger': '愤怒之咆哮精华',
        'shrieking-essence-of-torment': '折磨之咆哮精华',
        'shrieking-essence-of-sorrow': '哀惜之咆哮精华',
        'shrieking-essence-of-rage': '肆虐之咆哮精华',
        'shrieking-essence-of-suffering': '苦难之咆哮精华',
        'shrieking-essence-of-wrath': '雷霆之咆哮精华',
        'shrieking-essence-of-doubt': '疑惑之咆哮精华',
        'shrieking-essence-of-loathing': '厌恶之咆哮精华',
        'shrieking-essence-of-zeal': '热情之咆哮精华',
        'shrieking-essence-of-anguish': '煎熬之咆哮精华',
        'shrieking-essence-of-spite': '刻毒之咆哮精华',
        'shrieking-essence-of-scorn': '傲视之咆哮精华',
        'shrieking-essence-of-envy': '忌妒之咆哮精华',
        'shrieking-essence-of-misery': '凄惨之咆哮精华',
        'shrieking-essence-of-dread': '忌惮之咆哮精华',

        'screaming-essence-of-greed': '贪婪之哀嚎精华',
        'screaming-essence-of-contempt': '轻视之哀嚎精华',
        'screaming-essence-of-hatred': '憎恨之哀嚎精华',
        'screaming-essence-of-woe': '悲痛之哀嚎精华',
        'screaming-essence-of-fear': '恐惧之哀嚎精华',
        'screaming-essence-of-anger': '愤怒之哀嚎精华',
        'screaming-essence-of-torment': '折磨之哀嚎精华',
        'screaming-essence-of-sorrow': '哀惜之哀嚎精华',
        'screaming-essence-of-rage': '肆虐之哀嚎精华',
        'screaming-essence-of-suffering': '苦难之哀嚎精华',
        'screaming-essence-of-wrath': '雷霆之哀嚎精华',
        'screaming-essence-of-doubt': '疑惑之哀嚎精华',
        'screaming-essence-of-loathing': '厌恶之哀嚎精华',
        'screaming-essence-of-zeal': '热情之哀嚎精华',
        'screaming-essence-of-anguish': '煎熬之哀嚎精华',
        'screaming-essence-of-spite': '刻毒之哀嚎精华',
        'screaming-essence-of-scorn': '傲视之哀嚎精华',
        'screaming-essence-of-envy': '忌妒之哀嚎精华',
        'screaming-essence-of-misery': '凄惨之哀嚎精华',
        'screaming-essence-of-dread': '忌惮之哀嚎精华',
        
        # 催化剂
        'imbued-catalyst': '灌注催化剂',
        'abrasive-catalyst': '研磨催化剂',
        'noxious-catalyst': '有害催化剂',
        'accelerating-catalyst': '加速催化剂',
        'turbulent-catalyst': '猛烈催化剂',
        'unstable-catalyst': '不稳定的催化剂',
        'tempering-catalyst': '回火催化剂',
        'intrinsic-catalyst': '内在催化剂',
        'fertile-catalyst': '丰沃催化剂',
        'prismatic-catalyst': '棱光催化剂'
        # 圣甲虫
        # keep all
    }

    global_item_value_dir = {}
    for name, value in all_json.items():
        for english, chinese in chinese_english_alias_dir.items():
            if english == name:
                global_item_value_dir[chinese] = float(value)

    # print(global_item_value_dir)
    # for key, value in global_item_value_dir.items():
    #     if key == '':
    #         print(value)

    return global_item_value_dir


if __name__ == "__main__":

    league_name = "Affliction"
    get_global_data(league_name)


