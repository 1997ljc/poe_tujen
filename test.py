# import pyperclip
#
# pyperclip.copy('')

import keyboard

def my_function():
    print("快捷键被触发！")

# 注册 Ctrl+Shift+A 快捷键
keyboard.add_hotkey('space', my_function)

# 阻塞程序，直到按下 Esc 键
keyboard.wait('esc')