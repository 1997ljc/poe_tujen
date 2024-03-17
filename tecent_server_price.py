import base64
import gzip
import io
import json

import requests


# 巴兰的要塞
# 裂界守卫：约束
# 裂界守卫：净世
# 裂界守卫：寂灭
# 裂界守卫：奴役

def load_Tencent_Server_Data():
    Tencent_Server_Url = "https://gitee.com/hhzxxx/exilence-next-tx-release/raw/master/price2.txt"
    try:
        Tencent_Server_Data = requests.get(Tencent_Server_Url, verify=False).text
        # TODO: 需要添加在日志窗口的网页响应码输出
        compressed_bytes = base64.b64decode(str(Tencent_Server_Data).encode("utf-8-sig"))
        with gzip.GzipFile(fileobj=io.BytesIO(compressed_bytes), mode='rb') as f:
            decompressed_bytes = f.read()
        decompressed_json = decompressed_bytes.decode('utf-8')
        decompressed_data = json.loads(decompressed_json)

        all_price_json = {}

        for each_dir in decompressed_data:
            # 印记是永久区的？
            if each_dir["frameType"] not in [6, 2, 3, 1, 10, 9] and ("雾魇宝珠" not in each_dir['baseType']) and ("印记" != each_dir['baseType']) and ("强辅" not in each_dir['baseType']):
                all_price_json[each_dir['baseType']] = each_dir['calculated']

        return all_price_json
    except Exception as e:
        print(f"Error: {e}")
        raise e


if __name__ == "__main__":
    price_json = load_Tencent_Server_Data()  # 这是解码数据,price_josn里面就有数据了

    with open('./tencent_price_config.json', 'w', encoding="utf-8") as file:
        json.dump(price_json, file, ensure_ascii=False, indent=4)