import tkinter as tk
import pyautogui
import tkinter.filedialog as tkf
import json
import os

# currency_location left_up_location  right_down_location confirm_location right_path_location left_path_location
# global currency_location
# global left_up_location
# global right_down_location
# global confirm_location
# global right_path_location
# global left_path_location

global global_run_speed
global_run_speed = 2

global user_define_filter
global base_filter


def set_window(width, height, window, root):
    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口的左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 设置窗口的位置和大小
    window.geometry(f"{width}x{height}+{x}+{y}")


def set_location_0(root):
    window0 = tk.Toplevel(root)
    window0.title("设置位置1")
    set_window(350, 130, window0, root)
    label0 = tk.ttk.Label(window0, text="设置刷新货币位置！", style="poe_style.TLabel")
    label0.pack()

    def check_space(event):
        if event.keysym == "space":
            window0.destroy()
            x1, y1 = pyautogui.position()
            global currency_location
            currency_location = (x1, y1)

            set_location_1(root)

    window0.bind("<Key>", check_space)
    window0.focus_force()


def set_location_1(root):
    window1 = tk.Toplevel(root)
    window1.title("设置位置1")
    set_window(350, 130, window1, root)
    label1 = tk.ttk.Label(window1, text="设置第一列左上位置！", style="poe_style.TLabel")
    label1.pack()

    def check_space(event):
        if event.keysym == "space":
            window1.destroy()
            x1, y1 = pyautogui.position()
            global left_up_location
            left_up_location = (x1, y1)

            set_location_2(root)

    window1.bind("<Key>", check_space)
    window1.focus_force()


def set_location_2(root):
    window2 = tk.Toplevel(root)
    window2.title("设置位置2")
    set_window(350, 130, window2, root)
    label2 = tk.ttk.Label(window2, text="设置第二列右下位置！", style="poe_style.TLabel")
    label2.pack()

    def check_space(event):
        if event.keysym == "space":
            window2.destroy()
            x2, y2 = pyautogui.position()
            global right_down_location
            right_down_location = (x2, y2)

            set_location_3(root)

    window2.bind("<Key>", check_space)
    window2.focus_force()


def set_location_3(root):
    window3 = tk.Toplevel(root)
    window3.title("设置位置3")
    set_window(350, 130, window3, root)
    label3 = tk.ttk.Label(window3, text="设置<确定键>位置！", style="poe_style.TLabel")
    label3.pack()

    def check_space(event):
        if event.keysym == "space":
            window3.destroy()
            x3, y3 = pyautogui.position()
            global confirm_location
            confirm_location = (x3, y3)

            set_location_4(root)

    window3.bind("<Key>", check_space)
    window3.focus_force()

def set_location_4(root):
    window4 = tk.Toplevel(root)
    window4.title("设置位置4")
    set_window(350, 130, window4, root)
    label4 = tk.ttk.Label(window4, text="设置砍价条滑块中间位置！", style="poe_style.TLabel")
    label4.pack()

    def check_space(event):
        if event.keysym == "space":
            window4.destroy()
            x4, y4 = pyautogui.position()
            global right_path_location
            right_path_location = (x4, y4)

            set_location_5(root)

    window4.bind("<Key>", check_space)
    window4.focus_force()


def set_location_5(root):
    window5 = tk.Toplevel(root)
    window5.title("设置位置5")
    set_window(350, 130, window5, root)
    label5 = tk.ttk.Label(window5, text="设置砍价条左边沿位置！", style="poe_style.TLabel")
    label5.pack()

    def check_space(event):
        if event.keysym == "space":
            window5.destroy()
            x5, y5 = pyautogui.position()
            global left_path_location
            left_path_location = (x5, y5)

    window5.bind("<Key>", check_space)
    window5.focus_force()


def set_speed(root):

    show_set_speed_window = tk.Toplevel(root)
    show_set_speed_window.title("set_run_speed")
    set_window(350, 200, show_set_speed_window)
    # 输入框
    entry_speed = tk.Entry(show_set_speed_window, width=15, font=("Arial", 15))
    entry_speed.insert(0, "输入速度挡位,默认为2")  # 设置默认文本
    entry_speed.config(fg="gray")  # 设置前景色为白色，背景色为透明
    entry_speed.place(relx=0.5, rely=0.45, anchor="center")  # 输入框位置
    # 文本提示
    entry_speed_remind = tk.Label(show_set_speed_window, text="输入1(快)-1000(慢)的数字选择速度挡位！", font=("Courier", 12))
    entry_speed_remind.place(relx=0.5, rely=0.2, anchor="center")  # 设置提示文本
    button_confirm = tk.ttk.Button(show_set_speed_window, text=" \n  确定  \n ", command=lambda: get_run_speed(entry_speed, show_set_speed_window))
    button_confirm.place(relx=0.7, rely=0.75, anchor="center")  # 设置按钮的位置

def get_run_speed(entry_speed, show_set_speed_window):
    global global_run_speed
    try:
        run_speed = entry_speed.get()
        run_speed = int(run_speed)
        global_run_speed = run_speed

        if (run_speed > 1000) or (run_speed < 1):
            raise ValueError
        show_set_speed_window.destroy()
    except ValueError:
        # raise Error!
        speed_error_window = tk.Toplevel(show_set_speed_window)
        speed_error_window.title("输入错误！！！！")
        set_window(300, 300, speed_error_window)
        # 文本提示
        entry_speed_remind = tk.Label(speed_error_window, text="请输入1-1000的数字！！！！",font=("Courier", 12))
        entry_speed_remind.place(relx=0.5, rely=0.2, anchor="center")  # 设置提示文本


# def save_once_config():
#     once_list = [confirm_location, right_path_location, left_path_location]
#     with open(".location", "w", encoding="utf-8") as file:
#         for each in once_list:
#             file.write(f"{each[0]},{each[1]}")


def save_all_config(root):
    # 弹出保存文件对话框
    filepath = tkf.asksaveasfilename(
        defaultextension=".json",  # 默认文件扩展名
        initialfile="tujen.json",  # 设置默认文件名
        initialdir=os.getcwd(),
        filetypes=[("Json Files", "*.json"), ("All Files", "*.*")],  # 文件类型筛选
        title="保存配置文件",  # 对话框标题
    )
    try:
        config_data = {}
        location_list = [currency_location,
                         left_up_location,
                         right_down_location,
                         confirm_location,
                         right_path_location,
                         left_path_location]
        config_data["location"] = location_list
        config_data["global_run_speed"] = global_run_speed
        config_data["base_filter"] = base_filter
        config_data["user_define_filter"] = user_define_filter

        if filepath:
            # 用户选择了文件名，执行保存操作
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(config_data, file)

    except NameError:
        # 弹出窗口
        error_window = tk.Toplevel(root)
        error_window.title("请先设置坐标")
        set_window(200, 200, error_window, root)
        # 创建提示文本
        label_remind = tk.Label(error_window, text="\n\n\n\n请先设置坐标！！", font=("Courier", 15))
        label_remind.pack()


def read_all_config(root):
    # 弹出保存文件对话框
    filepath = tkf.askopenfilename(
        defaultextension=".json",  # 默认文件扩展名
        initialfile="tujen.json",  # 设置默认文件名
        initialdir=os.getcwd(),
        filetypes=[("Json Files", "*.json"), ("All Files", "*.*")],  # 文件类型筛选
        title="读取配置文件",  # 对话框标题
    )

    if filepath.strip() == '':
        print("用户取消了保存操作。")
    else:
        # 从配置文件加载状态
        try:
            with open(filepath, "r", encoding="utf-8") as config_file:
                config_data = json.load(config_file)
                # 读取出来数组
                # for compass_in_config, switch_in_config in config_data.items():
                #     for compass, data in compass_var_dir.items():
                #         if compass == compass_in_config:
                #             var = data[1]
                #             var.set(switch_in_config)
        except FileNotFoundError:
            file_error_window = tk.Toplevel(root)
            file_error_window.title("配置读取出错！")
            set_window(200, 200, file_error_window, root)
            file_error_label = tk.Label(file_error_window, text="配置文件不存在！！")
            file_error_label.pack()


def set_base_filter(root):
    base_filter = []


def set_user_define_filter(root):
    user_define_filter = []