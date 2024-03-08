import pyautogui
import time
import keyboard as kb
import random
import pyperclip
import tkinter as tk
import base_config

# def trade_with_tujen():


def auto_trade_all():
    config_set_window = tk.Toplevel(root)
    config_set_window.title("运行设置")
    base_config.set_window(300, 250, config_set_window, root)
    # 创建提示文本
    label_remind_all = tk.Label(config_set_window, text="第一次使用必须设置坐标！！", font=("Courier", 15))
    label_remind_all.place(relx=0.5, rely=0.1, anchor="center")  # 设置提示文本
    # 创建按钮
    button1 = tk.ttk.Button(config_set_window, text="设置坐标", command=lambda: base_config.set_location_0(root))
    button1.place(relx=0.25, rely=0.25, anchor="center")
    button2 = tk.ttk.Button(config_set_window, text="基础过滤", command=lambda: base_config.set_location_0(root))
    button2.place(relx=0.25, rely=0.5, anchor="center")
    button3 = tk.ttk.Button(config_set_window, text="读取设置", command=lambda: base_config.read_all_config(config_set_window))
    button3.place(relx=0.25, rely=0.75, anchor="center")
    button4 = tk.ttk.Button(config_set_window, text="设置速度", command=lambda: base_config.set_speed(config_set_window))
    button4.place(relx=0.75, rely=0.25, anchor="center")
    button5 = tk.ttk.Button(config_set_window, text="自定义过滤", command=lambda: base_config.set_user_define_filter(config_set_window))
    button5.place(relx=0.75, rely=0.5, anchor="center")
    button6 = tk.ttk.Button(config_set_window, text="保存设置", command=lambda: base_config.save_all_config(config_set_window))
    button6.place(relx=0.75, rely=0.75, anchor="center")


# def keep_trade(confirm_location, right_path_location, left_path_location, root):
def keep_trade_show(root):
    root.destroy()

    print(base_config.confirm_location)
    print(base_config.right_path_location)
    print(base_config.left_path_location)
    # 添加空格为快捷键
    kb.add_hotkey('space', keep_trade_wrapper)



def keep_trade_wrapper():

    relative_x = base_config.right_path_location[0] - base_config.left_path_location[0]
    relative_y = base_config.right_path_location[1] - base_config.left_path_location[1]

    pyautogui.moveTo(base_config.right_path_location[0], base_config.right_path_location[1], 0.1)
    pyautogui.mouseDown(base_config.right_path_location[0], base_config.right_path_location[1], 'left')
    time.sleep(0.1)  # 0.1 --- 0.2
    pyautogui.moveTo(base_config.left_path_location[0]+0.65 * relative_x, base_config.left_path_location[1], 0.1)
    pyautogui.mouseUp(base_config.left_path_location[0]+0.65 * relative_x, base_config.left_path_location[1], 'left')
    pyautogui.moveTo(base_config.confirm_location[0], base_config.confirm_location[1], 0.1)
    pyautogui.click(button="left")
    time.sleep(0.1)  # 0.1 --- 0.2
    pyautogui.click(button="left")

def auto_trade_once():
    config_set_window = tk.Toplevel(root)
    config_set_window.title("运行设置")
    base_config.set_window(200, 200, config_set_window, root)

    # 创建按钮
    button1 = tk.ttk.Button(config_set_window, text="设置坐标", command=lambda: base_config.set_location_3(config_set_window))
    button1.place(relx=0.4, rely=0.5, anchor="center")
    button2 = tk.ttk.Button(config_set_window, text="确定", command=lambda: keep_trade_show(config_set_window))
    button2.place(relx=0.7, rely=0.5, anchor="center")


# 创建主窗口
root = tk.Tk()
root.title("抄家模拟器")
base_config.set_window(250, 200, root, root)

# 定义窗口的标签风格
style = tk.ttk.Style()
style.configure("poe_style.TLabel", font=("Times new roman", 16))
# 创建提示文本
label_remind_1 = tk.Label(root, text="图金交易小助手v0.5", font=("Courier", 15))
label_remind_1.place(relx=0.5, rely=0.2, anchor="center")  # 设置提示文本

# 创建按钮
button1 = tk.ttk.Button(root, text="  \n狂暴模式\n  ", command=auto_trade_all)
button1.place(relx=0.3, rely=0.6, anchor="center")  # 设置按钮的位置
button2 = tk.ttk.Button(root, text="  \n小刀剌屁股\n  ", command=auto_trade_once)
button2.place(relx=0.7, rely=0.6, anchor="center")  # 设置按钮的位置


# 进入主事件循环
root.mainloop()
