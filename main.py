import json
import logging
import os
import re
import sys
import time
import tkinter as tk

import cv2
import keyboard as kb
import numpy as np
import pandas as pd
import pyautogui
import pyperclip

import base_config
import tecent_server_price as tsp
from base_config import gen_random_offset
from base_config import gen_random_time


# ==========================config function==========================
# 用于配置中，收集用户所进行的配置
def write_config(root, config, entry_list):

    try:
        # 对所有entry进行获取填入值
        entry_get_list = []
        for each_entry in entry_list:
            entry_get_list.append(int(each_entry.get()))

        entry_get_list_x = entry_get_list[:len(config['position'])]
        entry_get_list_y = entry_get_list[len(config['position']):2*len(config['position'])]
        entry_get_list_value = entry_get_list[2*len(config['position']):]
        # 所有新的值写回到配置中
        for key, value in zip(config['position'],entry_get_list_x):
            for key_p in config['position'][key].keys():
                if key_p == "x":
                    config['position'][key][key_p] = value

        for key, value in zip(config['position'],entry_get_list_y):
            for key_p in config['position'][key].keys():
                if key_p == "y":
                    config['position'][key][key_p] = value

        for key, value in zip(config["artifact"],entry_get_list_value):
            print(key)
            if key != "Background":
                for key_a in config['artifact'][key].keys():
                    if key_a == "value":
                        config['artifact'][key][key_a] = value

        # 再次存入配置文件
        with open(f'./location_config/all_config.json', 'w', encoding="utf-8") as file:
            json.dump(config, file, indent=4, ensure_ascii=False)

        config_window = base_config.attention_window(root, 150, 100, "设置成功",
                                     "设置成功！", 15, destort_root=1)

    except Exception as e:
        print(e)
        base_config.attention_window(root, 200, 200, "设置失败",
                                     "设置失败，请联系作者！", 15)


def set_user_define_config(root):
    try:
        # 各个位置坐标列表
        position_label_list = []
        position_list = []
        # 各个兑换通货列表
        artifact_label_list = []
        artifact_list = []
        # 所有输入框列表
        entry_list = []

        # 创建显示窗口
        config_window = tk.Toplevel(root)
        base_config.set_window(600, 500, config_window, config_window)
        label = tk.Label(config_window, text="配置完点击确定\n  再重启程序！！", font=("Times New Roman", 14))
        label.grid(row=1, column=2, rowspan=2, sticky="nsew")

        # 打开配置文件读取
        config_path = './location_config'
        with open(f'{config_path}/all_config.json', 'r', encoding="utf-8") as file:
            config = json.load(file)

        # 拿到文件目前的配置
        for key_p, value_p in config['position'].items():
            for key, value in value_p.items():
                if key == "x":
                    position_label_list.append(f'<{key_p}>-X :')
                    position_list.append(value)

        for key_p, value_p in config['position'].items():
            for key, value in value_p.items():
                if key == "y":
                    position_label_list.append(f'<{key_p}>-Y :')
                    position_list.append(value)

        for key_a, value_a in config["artifact"].items():
            if key_a != "Background":
                artifact_label_list.append(f'<{key_a}>兑换最低价值 :')
                artifact_list.append(value_a["value"])

        # 创建上述列表的标签和对应输入框，并使用 grid 布局管理器均匀分布
        for i in range(16):
            # 创建 Label 组件
            label = tk.Label(config_window, text=f"{position_label_list[i]}")
            label.grid(row=(2 * i) % 16, column=(2 * i) // 16, padx=5, pady=4)
            # 创建输入框，并设置对应的标签
            entry = tk.Entry(config_window)
            entry.grid(row=(2 * i + 1) % 16, column=(2 * i + 1) // 16, padx=5, pady=4)
            entry.insert(0, f"{position_list[i]}")  # 设置默认文本
            entry.config(fg="gray")  # 设置前景色为白色，背景色为透明
            entry_list.append(entry)

        for i in range(4):

            label = tk.Label(config_window, text=f"{artifact_label_list[i]}")
            label.grid(row=(2 * i) % 8 + 4, column=(2 * i) // 8 + 2, padx=5, pady=4)

            entry = tk.Entry(config_window)
            entry.grid(row=(2 * i + 1) % 8 + 4, column=(2 * i + 1) // 8 + 2, padx=5, pady=4)
            entry.insert(0, f"{artifact_list[i]}")  # 设置默认文本
            entry.config(fg="gray")  # 设置前景色为白色，背景色为透明

            entry_list.append(entry)
        # 创建保存按钮
        button2 = tk.ttk.Button(config_window, text="\n   确定   \n", command=lambda: write_config(config_window, config, entry_list))
        button2.grid(row=13, column=2, rowspan=2, sticky="nsew")

    #设置错误信息与弹窗
    except FileNotFoundError:
        error_window = base_config.attention_window(root, 200, 200, "加载失败",
                                                    "检查location_config文件夹中\n   是否有配置文件！",
                                                    12, destort_root=1)
    except Exception as e:
        print(f"error {e} in function set_user_define_config")


def load_config(root):
    try:
        # 加载所有截图
        image_path = './location_image'
        config_path = './location_config'

        with open(f'{config_path}/all_config.json', 'r', encoding="utf-8") as file:
            config = json.load(file)

        # 拿数据
        price_json = tsp.load_Tencent_Server_Data()
        config["price_json"] = price_json
        # 如果用户想要数据表格
        if int(config["save_price_data"]) == 1:
            # 数据转换并写入 Excel 文件给用户看
            series = pd.Series(price_json)
            df = pd.DataFrame(series, columns=["Value"])
            df.to_excel('./物品价格.xlsx', header=False)

        # 读取所有图片的imread信息存到config中
        for file in os.listdir(image_path):
            if file.split('.')[1] == 'jpg' and file.split('.')[0] != "temp":
                file_name = file.split('.')[0]
                config['artifact'][file_name]['img_msg'] = cv2.imread(f'{image_path}/{file}')

    except Exception as e:
        print(f"error {e} in function load_config")
        error_window = base_config.attention_window(root, 300, 300, "加载失败",
                                                    "加载失败，请检查网络\n（国服版不要开飞机）！",
                                                    15, destort_root=1)


    return config


def get_location():
    global all_config
    try:
        # 找到物品兑换时候出现的框体的位置，进行校准
        background_location = pyautogui.locateOnScreen(all_config["artifact"]['Background']['img_msg'])

        # 提取 Box 对象的左上角和右下角坐标
        left, top, width, height = background_location
        background_location_list = [int(left), int(top), int(width), int(height)]

        all_config["background_location_list"] = background_location_list

        base_config.attention_window(root, 150, 150, "校准成功！",
                                     "校准成功！\n请关闭此窗口！", 15, destort_root=0)

    except Exception as e:
        base_config.attention_window(root, 150, 150, "校准失败！",
                                     "请露出整个\n 兑换面板！", 15, destort_root=0)
        print(f"error {e} in function get_location")

# ==========================config function==========================

# ==========================auto trade more function==========================
# 用户输入兑换通货的数量
def set_coinage(root):

    set_coinage_window = tk.Toplevel(root)
    base_config.set_window(200,200,set_coinage_window,set_coinage_window)

    label = tk.Label(set_coinage_window, text=f"设置刷新货币数量", font=("Times New Roman", 15))
    label.place(relx=0.5, rely=0.3, anchor="center")

    entry = tk.Entry(set_coinage_window)
    entry.place(relx=0.5, rely=0.5, anchor="center")
    entry.insert(0, f"1")  # 设置默认文本
    entry.config(fg="gray")  # 设置前景色为白色，背景色为透明

    button = tk.ttk.Button(set_coinage_window, text="确定并开始", command=lambda: jugg_it(entry, set_coinage_window))
    button.place(relx=0.5, rely=0.7, anchor="center")


def jugg_it(entry, set_coinage_window):

    try:
        if not entry.get().isdigit():
            set_coinage_window.destroy()
            coinage_number = 0
            raise ValueError
        else:
            # 刷新货币数目
            coinage_number = int(entry.get())
            set_coinage_window.destroy()

    except Exception as e:
        base_config.attention_window(root, 150, 150, "数据异常！",
                                     "请输入数字！", 15, destort_root=0)
        print(f"error {e} in function jugg_it")

    # 拿到所有兑换通货的图片数据以及每种通货对应物品的最低价值，还有各个坐标的位置
    left_up_x, left_up_y = all_config["position"]["left_up"]["x"], all_config["position"]["left_up"]["y"]
    second_right_down_x, second_right_down_y = all_config["position"]["second_right_down"]["x"], \
    all_config["position"]["second_right_down"]["y"]
    confirm_button_x, confirm_button_y = all_config["position"]["confirm_button"]["x"], \
    all_config["position"]["confirm_button"]["y"]
    right_haggle_x, right_haggle_y = all_config["position"]["right_haggle"]["x"], \
    all_config["position"]["right_haggle"]["y"]
    left_haggle_x, left_haggle_y = all_config["position"]["left_haggle"]["x"], all_config["position"]["left_haggle"][
        "y"]
    coinage_roll_x, coinage_roll_y = all_config["position"]["coinage_roll"]["x"], \
    all_config["position"]["coinage_roll"]["y"]
    null_space_x, null_space_y = all_config["position"]["null_space"]["x"], all_config["position"]["null_space"][
        "y"]
    close_button_x, close_button_y = all_config["position"]["close_button"]["x"], \
        all_config["position"]["close_button"]["y"]

    # 点击空白处激活窗口
    pyautogui.moveTo(gen_random_offset(null_space_x), gen_random_offset(null_space_y), gen_random_time(speed))
    pyautogui.click(button="left")

    # 设置每一步的步长，以及整个循环跳出的flag
    y_step = (second_right_down_y - left_up_y) / 10
    x_step = second_right_down_x - left_up_x
    # 中途结束标志位，跳出循环用
    break_flag = 0
    # 当前面板全部兑换完成标志位，跳出循环用
    finish_flag = 0

    # 主要循环体，取物品
    for coinage in range(coinage_number + 1):

        print(f"总{coinage_number + 1}次面板兑换，第{coinage + 1}次开始")

        for x_num in range(2):
            for y_num in range(11):
                # 程序运行中结束程序
                if kb.is_pressed('end'):
                    print("结束键被按下,程序终止！！！")
                    # 加一些延时
                    time.sleep(0.001)
                    break_flag = 1
                    break
                else:
                    # 鼠标放到物品上，复制物品属性
                    pyautogui.moveTo(gen_random_offset(left_up_x + x_step * x_num),
                                     gen_random_offset(left_up_y + y_step * y_num), gen_random_time(speed))
                    time.sleep(gen_random_time(speed))
                    # 将剪贴板中的内容取出并赋值给content
                    pyautogui.hotkey("ctrl", "alt", "c")
                    content = pyperclip.paste()
                    time.sleep(gen_random_time(speed))
                    # debug 打印
                    # print(content)

                    try:

                        # 数量判断
                        if '可堆叠通货' in content:
                            item_amount = content[
                                          (content.find('堆叠数量: ') + len('堆叠数量: ')):content.find("/")].replace(" ", "")
                            item_amount = int(item_amount)
                        else:
                            item_amount = 1

                        # 是否命中用户需要无脑保留或者无脑丢弃的物品
                        always_flag = 0

                        # 用户自定义无脑保留哪些物品，支持正则
                        for each in all_config["AlwaysKeep"]:
                            match = re.search(each, content)
                            if match:
                                item_name = f'无脑保留的{each}'
                                item_value = 999999
                                always_flag = 1
                                break
                        # 用户自定义无脑丢弃哪些物品，支持正则
                        for each in all_config["AlwaysDrop"]:
                            match = re.search(each, content)
                            if match:
                                item_name = f'无脑丢弃的{each}'
                                item_value = 0.000001
                                always_flag = 1
                                break

                        # 根据标志位判断，如果已经命中了用户需要无脑保留的，那么就不用进行后面的判断了
                        if always_flag == 0:
                            # 物品判断及其价值判断
                            # price_json数据格式为字典 名称：价格
                            if '物品类别: 可堆叠通货' in content:
                                if "混沌石" in content:
                                    item_name = '混沌石'
                                    item_value = 1
                                if "梦魇拟像裂片" in content:
                                    item_name = '梦魇拟像裂片'
                                    item_value = all_config["price_json"]['梦魇拟像'] / 300.0
                                elif "驱灵裂片" in content:
                                    item_name = '驱灵裂片'
                                    item_value = all_config["price_json"]['驱灵法器'] / 100.0
                                elif "剥离石碎片" in content:
                                    item_name = '剥离石碎片'
                                    item_value = all_config["price_json"]['剥离石'] / 100.0
                                elif "平行石碎片" in content:
                                    item_name = '平行石碎片'
                                    item_value = all_config["price_json"]['平行石'] / 20.0
                                elif "先驱石碎片" in content:
                                    item_name = '先驱石碎片'
                                    item_value = all_config["price_json"]['先驱石'] / 20.0
                                elif ("永恒" in content) and ("裂片" in content):
                                    # 对五个军团裂片进行替换
                                    match = re.search(r'永恒(.{2,7})裂片', content)
                                    if match:
                                        # 如果找到匹配的部分，则返回匹配到的部分
                                        item_name = "永恒" + match.group(1) + "印记的碎片"
                                        item_value = all_config["price_json"][f"永恒{match.group(1)}印记"] / 100.0
                                    else:
                                        raise ValueError
                                elif "裂隙碎片" in content:
                                    # 对五个裂隙碎片进行替换
                                    match = re.search(r'裂隙碎片\((.{2,7})\)', content)
                                    if match:
                                        # 如果找到匹配的部分，则返回匹配到的部分
                                        item_name = match.group(1) + "裂隙石的碎片"
                                        item_value = all_config["price_json"][f"{match.group(1)}裂隙石"] / 100.0
                                    else:
                                        raise ValueError
                                else:
                                    for name, value in all_config["price_json"].items():
                                        if name in content:
                                            item_name = name
                                            item_value = value
                            elif "物品类别: 孕育石" in content:
                                item_name = '孕育石'
                                item_value = 0.00000001
                            elif '物品类别: 技能宝石' in content:
                                if '等级: 21' in content or '+20%' in content or '+23%' in content:
                                    for name, value in all_config["price_json"].items():
                                        if name in content:
                                            item_name = name
                                            item_value = value
                                else:
                                    item_name = "垃圾宝石"
                                    item_value = 0.00000001
                            elif '物品类别: 辅助宝石' in content:
                                if '启蒙' in content or '赋予' in content or '增幅' in content:
                                    item_name = '卓越宝石'
                                    item_value = '10000'
                                elif '等级: 21' in content or '+20%' in content or '+23%' in content:
                                    for name, value in all_config["price_json"].items():
                                        if name in content:
                                            item_name = name
                                            item_value = value
                                else:
                                    item_name = "垃圾宝石"
                                    item_value = 0.00000001
                            elif '物品类别: 深渊珠宝' in content:
                                if ('等阶：1' in content) and (
                                        ('最大生命' in content) or ('能量护盾' in content) or ('全域暴击伤害加成' in content)):
                                    item_name = '深渊珠宝'
                                    item_value = 10000
                                else:
                                    item_name = '垃圾深渊珠宝'
                                    item_value = 0.000001
                            elif '物品类别: 蓝图' in content:
                                item_name = '蓝图'
                                item_value = 10000
                            elif '物品类别: 契约' in content:
                                if '欺诈' in content:
                                    item_name = '欺诈契约'
                                    item_value = 10000
                                if '解密术' in content:
                                    item_name = '解密术契约'
                                    item_value = 1
                                else:
                                    item_name = '垃圾契约'
                                    item_value = 0.00001
                            elif '星团珠宝' in content and (('物品等级: 84' in content) or ('物品等级: 85' in content)):
                                if ("6 个" in content) or ("8 个" in content) or ("12 个" in content) or ("3 个" in content):
                                    item_name = '有用星团'
                                    item_value = 10000
                                else:
                                    item_name = "垃圾星团"
                                    item_value = 0.000001
                            elif "裂隙戒指" in content:
                                if ('物品等级: 84' in content) or ('物品等级: 85' in content) or ('物品等级: 86' in content):
                                    item_name = '裂隙戒指（换扼杀）'
                                    item_value = 12
                                else:
                                    item_name = '裂隙戒指（没用）'
                                    item_value = 0.0000001
                            elif '物品类别: 异界地图' in content:
                                if "脑层" in content:
                                    item_name = "脑层"
                                    item_value = all_config["price_json"]["脑层"]
                                elif "不死鸟锻台" in content:
                                    item_name = "不死鸟锻台"
                                    item_value = all_config["price_json"]["不死鸟锻台"]
                                elif "牛头人迷宫" in content:
                                    item_name = "牛头人迷宫"
                                    item_value = all_config["price_json"]["牛头人迷宫"]
                                elif "奇美拉领域" in content:
                                    item_name = "奇美拉领域"
                                    item_value = all_config["price_json"]["奇美拉领域"]
                                elif "九头蛇巢穴" in content:
                                    item_name = "九头蛇巢穴"
                                    item_value = all_config["price_json"]["九头蛇巢穴"]
                                elif '裂界守卫' in content:
                                    item_name = "裂界守卫地图"
                                    item_value = 10000
                                elif '的要塞' in content:
                                    item_name = "希鲁斯守卫地图"
                                    item_value = 10000
                                else:
                                    item_name = "垃圾地图"
                                    item_value = 0.000001
                            elif '物品类别: 地图碎片' in content:
                                for name, value in all_config["price_json"].items():
                                    if name in content:
                                        item_name = name
                                        item_value = value
                            elif content == '':
                                print(f"当前面板兑换结束！\n总{coinage_number + 1}次，第{coinage + 1}次结束")
                                finish_flag = 1
                                break
                            else:
                                item_name = f'未找到如下物品！:\n{content}'
                                raise ValueError
                    except ValueError:
                        print(f"{content}数据错误")
                        base_config.attention_window(root, 400, 400, "未知物品",
                                                     "出现未知物品，请保存当前目录下\nterminal日志文件并联系作者", 8, destort_root=1)

                # 按下弹出通货界面，进行对比
                # pyautogui.moveTo(left_up_x + x_step * x_num, left_up_y + y_step * y_num, gen_random_time(speed))
                time.sleep(gen_random_time(speed))  # 0.1 --- 0.2
                pyautogui.click(button="left")

                # 把中间那片截图的地方给划定出来
                try:
                    pyautogui.screenshot('./location_image/temp.jpg', region=all_config['background_location_list'])
                    haggle_image = cv2.imread('./location_image/temp.jpg')
                except KeyError:
                    window_key_error = tk.Toplevel(root)
                    window_key_error.title("配置错误")
                    base_config.set_window(200, 200, window_key_error, window_key_error)
                    window_key_error.attributes('-topmost', True)
                    label_key_error = tk.Label(window_key_error, text="请先进行定位！", font=("Courier", 15))
                    label_key_error.place(relx=0.5, rely=0.1, anchor="center")  # 设置提示文本

                # 截图并与所有兑换通货进行对比
                thresh = 0.8
                for key, value in all_config["artifact"].items():
                    if key != 'Background':
                        img_gray = cv2.cvtColor(value['img_msg'], cv2.COLOR_BGR2GRAY)
                        temp_gray = cv2.cvtColor(haggle_image, cv2.COLOR_BGR2GRAY)

                        res = cv2.matchTemplate(image=img_gray, templ=temp_gray, method=cv2.TM_CCOEFF_NORMED)
                        loc = np.where(res >= thresh)

                        if len(loc[0]) > 0:
                            haggle_value = value['value']
                            haggle_currency = key
                            break
                        else:
                            haggle_currency = None
                            haggle_value = 987654321
                # 程序运行中结束程序
                if kb.is_pressed('end'):
                    print("结束键被按下,程序终止！！！")
                    # 加一些延时
                    time.sleep(0.001)
                    break_flag = 1
                    break
                else:
                    # 判断当前物品价值是否大于所用的兑换通货的最低价值
                    print(f"发现物品<{item_name}x{item_amount}>,价值{item_amount * item_value},使用兑换通货{haggle_currency}最低价值要求为{haggle_value}")
                    if (item_amount * item_value) >= haggle_value:
                        print(f"<{item_name}x{item_amount}>保留！")

                        pyautogui.moveTo(gen_random_offset(right_haggle_x), gen_random_offset(right_haggle_y), gen_random_time(speed))
                        pyautogui.mouseDown(right_haggle_x, right_haggle_y, 'left')
                        time.sleep(gen_random_time(speed))
                        pyautogui.moveTo(gen_random_offset(left_haggle_x + 0.65 * (right_haggle_x - left_haggle_x)), left_haggle_y, gen_random_time(speed))
                        pyautogui.mouseUp(gen_random_offset(left_haggle_x + 0.65 * (right_haggle_x - left_haggle_x)), left_haggle_y, 'left')
                        pyautogui.moveTo(gen_random_offset(confirm_button_x), gen_random_offset(confirm_button_y), gen_random_time(speed))
                        pyautogui.click(button="left")
                        time.sleep(gen_random_time(speed))
                        pyautogui.click(button="left")
                    else:
                        print(f"<{item_name}x{item_amount}>丢弃！")
                        # 鼠标移到关闭按钮，关闭兑换界面
                        pyautogui.moveTo(gen_random_offset(close_button_x, 0.5), gen_random_offset(close_button_y, 0.5), gen_random_time(speed))
                        pyautogui.click(button="left")

                # 清除本次判断的物品，方便下一个格子判断是否有东西
                # TODO： 四格共振器需要解决一下
                pyperclip.copy("")

            # 判断当前面板是否被兑换完毕,或者按下终止键
            if (break_flag == 1) or (finish_flag == 1):
                # 当上一次面板兑换完之后，需要把finish_flag清零，否则下一次第二列将会直接跳出
                finish_flag = 0
                break

        # 判断是否有程序终止按键,如果没有的话就重新刷新一下
        if break_flag == 1:
            break
        else:
            # 如果是最后一次就不刷新面板了
            if coinage != (coinage_number + 1):
                pyautogui.moveTo(gen_random_offset(coinage_roll_x), gen_random_offset(coinage_roll_y), gen_random_time(speed))
                pyautogui.click(button="left")

# ==========================auto trade more function==========================
# ==========================auto trade once function==========================


def auto_trade_once_function(position_list, mouse_back_enable):
    origin_x, origin_y = pyautogui.position()
    pyautogui.click(button="left")
    pyautogui.moveTo(gen_random_offset(position_list[0]), position_list[1], gen_random_time(speed))
    pyautogui.mouseDown(position_list[0], position_list[1], 'left')
    time.sleep(gen_random_time(speed))  # 0.1 --- 0.2
    pyautogui.moveTo(gen_random_offset(position_list[2] + 0.65 * (position_list[1] - position_list[2])), position_list[3], gen_random_time(speed))
    pyautogui.mouseUp(gen_random_offset(position_list[2] + 0.65 * (position_list[1] - position_list[2])), position_list[3], 'left')
    pyautogui.moveTo(gen_random_offset(position_list[4]), gen_random_offset(position_list[5], 1), gen_random_time(speed))
    pyautogui.click(button="left")
    time.sleep(gen_random_time(speed))  # 0.1 --- 0.2
    pyautogui.click(button="left")
    # 如果鼠标返回使能则回到之前的点
    if mouse_back_enable:
        pyautogui.moveTo(origin_x, origin_y, gen_random_time(speed))


def auto_trade_once_confirm(position_list, auto_trade_window, mouse_back_enable):
    global add_hotkey_flag
    if add_hotkey_flag:
        kb.remove_hotkey('space')

    kb.add_hotkey('space', lambda: auto_trade_once_function(position_list, mouse_back_enable))
    add_hotkey_flag = 1

    # 关闭窗口
    auto_trade_window.destroy()


def auto_trade_once_remove(auto_trade_window):
    global add_hotkey_flag
    if add_hotkey_flag:
        # 去掉空格绑定的函数
        kb.remove_hotkey('space')
        add_hotkey_flag = 0
    auto_trade_window.destroy()


def auto_trade_once(root):
    global all_config
    right_haggle_x, right_haggle_y = all_config["position"]["right_haggle"]["x"], \
    all_config["position"]["right_haggle"]["y"]
    left_haggle_x, left_haggle_y = all_config["position"]["left_haggle"]["x"], all_config["position"]["left_haggle"][
        "y"]
    confirm_button_x, confirm_button_y = all_config["position"]["confirm_button"]["x"], \
    all_config["position"]["confirm_button"]["y"]

    position_list = [right_haggle_x, right_haggle_y, left_haggle_x, left_haggle_y,
                     confirm_button_x, confirm_button_y]

    auto_trade_window = tk.Toplevel(root)
    auto_trade_window.title("确认")
    base_config.set_window(200, 150, auto_trade_window, root)
    # 创建按钮
    button1 = tk.ttk.Button(auto_trade_window, text="点击开启", command=lambda: auto_trade_once_confirm(position_list,
                                                                                                     auto_trade_window,
                                                                                                     var.get()))
    button1.place(relx=0.3, rely=0.3, anchor="center")

    button2 = tk.ttk.Button(auto_trade_window, text="用完点我关闭", command=lambda: auto_trade_once_remove(auto_trade_window))
    button2.place(relx=0.5, rely=0.6, anchor="center")

    # 创建复选框，是否使能鼠标回原位的功能
    var = tk.IntVar()
    checkbutton = tk.Checkbutton(auto_trade_window, text=f"鼠标返回", variable=var)
    checkbutton.place(relx=0.7, rely=0.3, anchor="center")

# ==========================auto trade once function==========================

# ==========================get position function==========================
def show_position():
    x, y = pyautogui.position()
    position_log_tab2.insert(tk.END, f"当前位置为x:{x},y:{y}" + '\n')  # 在末尾插入日志消息
    position_log_tab2.see(tk.END)  # 滚动到末尾


def tab_changed(event):
    selected_tab = notebook.index(notebook.select())
    if selected_tab == 0:
        root.attributes('-topmost', False)
    elif selected_tab == 1:
        root.attributes('-topmost', True)
        kb.add_hotkey('space', show_position)
# ==========================get position function==========================


# 创建主窗口
root = tk.Tk()
root.title("抄家模拟器")
base_config.set_window(300, 300, root, root)

# 设置日志格式
logging.basicConfig(filename='terminal.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# 重定向标准输出和标准错误输出到日志文件
sys.stdout = open('terminal.log', 'w')
sys.stderr = open('terminal.log', 'w')

# 保存所有从文件中读取的函数
global all_config
all_config = {}
all_config = load_config(root)
global speed
speed = int(all_config['speed(1-20)'])

# 是否已经绑定了单个物品手动拖动滚动条的函数标志，方便后面remove
global add_hotkey_flag
add_hotkey_flag = 0

# 定义窗口的标签风格
style = tk.ttk.Style()
style.configure("poe_style.TLabel", font=("Times new roman", 16))

# 创建两个标签页面，一个是主程序，另一个是获取坐标
style.configure('TNotebook.Tab', font=('Times new roman', 14))
notebook = tk.ttk.Notebook(root)
tab1 = tk.ttk.Frame(notebook)
notebook.add(tab1, text="主界面")
tab2 = tk.ttk.Frame(notebook)
notebook.add(tab2, text="获取坐标")
notebook.pack(expand=True, fill='both')
# 绑定标签页切换事件,获取坐标就执行获取坐标的函数
notebook.bind("<<NotebookTabChanged>>", tab_changed)

# 标签页1内容如下：
# 创建提示文本
label_remind_1 = tk.Label(tab1, text="图金交易小助手v0.5", font=("Courier", 15))
label_remind_1.place(relx=0.5, rely=0.1, anchor="center")  # 设置提示文本
label_remind_2 = tk.Label(tab1, text="\n\n国服数据来源易刷E-farm\nE-farm在线人数越多,价格越精确\n请多多支持！\n\n", font=("Courier", 10))
label_remind_2.place(relx=0.5, rely=0.8, anchor="center")  # 设置提示文本

# 创建按钮
button1 = tk.ttk.Button(tab1, text="  \n按我进行定位\n  ", command=get_location)
button1.place(relx=0.3, rely=0.3, anchor="center")  # 设置按钮的位置
button2 = tk.ttk.Button(tab1, text="  \n点我更改配置\n  ", command=lambda: set_user_define_config(root))
button2.place(relx=0.7, rely=0.3, anchor="center")  # 设置按钮的位置
button3 = tk.ttk.Button(tab1, text="  \n你帮我拿\n  ", command=lambda: set_coinage(root))
button3.place(relx=0.3, rely=0.55, anchor="center")  # 设置按钮的位置
button4 = tk.ttk.Button(tab1, text="  \n我自己选\n  ", command=lambda: auto_trade_once(root))
button4.place(relx=0.7, rely=0.55, anchor="center")  # 设置按钮的位置

# 标签页2内容如下：
# 创建提示文本
label_tab2 = tk.Label(tab2, text="按空格获取位置", font=("Courier", 15))
label_tab2.place(relx=0.5, rely=0.2, anchor="center")  # 设置提示文本
# 创建日志框
position_log_tab2 = tk.Text(tab2, wrap=tk.WORD, height=7, width=25)
position_log_tab2.place(relx=0.5, rely=0.6, anchor="center")  # 设置日志框的位置

# 进入主事件循环
root.mainloop()
