import tkinter as tk

import keyboard as kb
import pyautogui


def log_message(message):
    position_log.insert(tk.END, message + '\n')  # 在末尾插入日志消息
    position_log.see(tk.END)  # 滚动到末尾


def set_window(width, height, window):
    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口的左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 设置窗口的位置和大小
    window.geometry(f"{width}x{height}+{x}+{y}")


def show_position():
    x, y = pyautogui.position()
    log_message(f"当前位置为x:{x},y:{y}")


if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    root.title("坐标获取")
    # 设置基础设置窗口为置顶
    root.attributes('-topmost', True)
    kb.add_hotkey('space', show_position)
    set_window(250, 200, root)
    # 创建提示文本
    label = tk.Label(root, text="按空格获取位置", font=("Courier", 15))
    label.place(relx=0.5, rely=0.2, anchor="center")  # 设置提示文本

    # 创建日志框
    position_log = tk.Text(root, wrap=tk.WORD, height=7, width=25)
    position_log.place(relx=0.5, rely=0.6, anchor="center")  # 设置日志框的位置

    root.mainloop()