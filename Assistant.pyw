# -*- coding: utf-8 -*-
import string
import datetime
from tkinter import ttk, HORIZONTAL
from tkinter import PhotoImage
from tkinter import Toplevel, Entry, Label
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import time
import os
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

if getattr(sys, 'frozen', None):
    basedir = sys._MEIPASS  # 打包后用的这个路径
    # print(basedir)
else:
    basedir = os.path.dirname(
        __file__)  # 直接运行的时候用的这个#  通过这种写法就可以实现打包和当前调试都可以运行with open(os.path.join(basedir, 'a.txt'), 'r', encoding='utf-8') as f:d = f.read()print(d)
    # print(basedir)

sys.path.append(basedir)
from lunardate import LunarDate
import VPN_Login
import webbrowser
import psutil
import sqlite3
import random
import copy

# 连接数据库
conn = sqlite3.connect(os.path.join(basedir, 'gui.db'))
cursor = conn.cursor()


def connect_vpn(name):
    VPN_Login.VPN().run(company=name)


class LoginGUI:
    def __init__(self, master):
        self.master = master
        master.title("项目助手数据库版V0.01")
        master.iconbitmap(os.path.join(basedir, 'Goomba.ico'))
        GUI_img = Image.open(os.path.join(basedir, 'bg.png'))
        GUI_w, GUI_h = GUI_img.size
        master.geometry(f"{GUI_w}x{GUI_h}")

        # 读取公司数据
        self.companies = {}

        cursor.execute("SELECT Function_Name, Function_Code FROM function WHERE Function__Level='2'")
        com_names = cursor.fetchall()

        for com_name, com_code in com_names:
            cursor.execute(
                "SELECT Function_Name, Function_Code FROM function WHERE Function__Superior=? AND Function__Level='3'",
                (com_code,))
            pro_names = cursor.fetchall()

            for pro_name, pro_code in pro_names:
                cursor.execute(
                    "SELECT Function_Name, Function_Code FROM function WHERE Function__Superior=? AND Function__Level='4'",
                    (pro_code,))
                web_names = cursor.fetchall()

                for web_name, web_code in web_names:
                    cursor.execute("SELECT Tools_Path FROM Tools WHERE Function_Code=?", (web_code,))
                    web_addr = cursor.fetchone()[0]

                    cursor.execute(
                        "SELECT Function_Url, Function_User, Function_Password FROM Function_Users WHERE Function_Code=?",
                        (pro_code,))
                    vpn_data = cursor.fetchone()

                    cursor.execute("SELECT Info FROM Info WHERE Function_Code=?", (pro_code,))
                    web_info = cursor.fetchone()[0]

                    com_name, pro_name, VPN_addr, VPN_user, VPN_pwd, web_name, web_addr, web_info = com_name, pro_name, \
                    vpn_data[0], vpn_data[1], vpn_data[2], web_name, web_addr, web_info
                    self.companies[web_name, web_addr] = (com_name, pro_name, VPN_addr, VPN_user, VPN_pwd, web_info)
                    # print((com_name, pro_name, VPN_addr, VPN_user, VPN_pwd, web_info))
        self.create_widgets()
        self.display_homepage()

    def create_widgets(self):
        # 菜单栏
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="替换背景图片", command=self.select_bg_image)
        file_menu.add_command(label="系统清理", command=self.select_sys_clean)
        file_menu.add_command(label="网络重置", command=self.select_net_clean)
        menubar.add_cascade(label="文件", menu=file_menu)
        topmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="网站", menu=topmenu)
        topmenu.add_command(label="打开网站", command=self.open_url)

        self.text = tk.Text(self.master, height=10)
        self.text.pack()
        self.save_btn = ttk.Button(self.master)
        self.save_btn.pack()

        # 当前时间
        self.time_var = tk.StringVar()
        self.time_label = tk.Label(self.master, textvariable=self.time_var)
        self.time_label.place(relx=0.5, rely=0.99, anchor='center')
        self.refresh()

        # 背景图片
        self.bg_image = ImageTk.PhotoImage(Image.open(os.path.join(basedir, 'bg.png')))
        self.bg_label = tk.Label(self.master, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 页面框架
        self.page_frame = ttk.Frame(self.master)
        self.page_frame.pack(side='left', padx=100, pady=20)

    def display_homepage(self):
        # 清空页面框架
        for widget in self.page_frame.winfo_children():
            widget.destroy()

        self.text.destroy()
        self.save_btn.destroy()
        self.time_label.destroy()

        # 显示所有公司信息
        list1 = []
        for (web_name, web_addr), (com_name, pro_name, VPN_addr, VPN_user, VPN_pwd, web_info) in self.companies.items():
            details = com_name
            list1.append(details)
        set1 = set(list1)
        set11 = sorted(set1)
        row = 0
        for com_name in set11:
            b1 = ttk.Button(self.page_frame, text=com_name, compound="left",
                            command=lambda name=com_name: self.display_company(name))
            b1.grid(row=row, column=0, sticky="ew", padx=10, pady=10)

            row += 1
            # print(com_name)

        # 维护按钮
        ttk.Button(self.page_frame, text="更新信息", command=self.maintain_information).grid(row=row, column=0,
                                                                                             sticky="ew",
                                                                                             padx=10, pady=10)
        ttk.Button(self.page_frame, text="增加信息", command=self.create_add_data_form).grid(row=row + 1, column=0,
                                                                                             sticky="ew",
                                                                                             padx=10, pady=10)

        # 当前时间
        self.time_label = ttk.Label(self.master, textvariable=self.time_var)
        self.time_label.place(relx=0.5, rely=0.99, anchor='center')

    # 从数据库抓取当前数据的函数
    def fetch_current_data(self):
        # 获取数据（根据你的表和列名调整SQL语句）
        # 读取公司数据
        cursor.execute("SELECT ID,Function_Name, Function_Code FROM function WHERE Function__Level='2'")
        com_names = cursor.fetchall()

        list_assistant = []

        for com_id, com_name, com_code in com_names:
            cursor.execute(
                "SELECT ID,Function_Name, Function_Code FROM function WHERE Function__Superior=? AND Function__Level='3'",
                (com_code,))
            pro_names = cursor.fetchall()
            # print(pro_names)

            for pro_id, pro_name, pro_code in pro_names:
                cursor.execute(
                    "SELECT ID,Function_Name, Function_Code FROM function WHERE Function__Superior=? AND Function__Level='4'",
                    (pro_code,))
                web_names = cursor.fetchall()

                my_dict = {}

                for web_name_id, web_name, web_code in web_names:
                    cursor.execute("SELECT ID,Tools_Path FROM Tools WHERE Function_Code=?", (web_code,))
                    web_addr = cursor.fetchone()
                    # print(web_addr)

                    cursor.execute(
                        "SELECT ID,Function_Url, Function_User, Function_Password FROM Function_Users WHERE Function_Code=?",
                        (pro_code,))
                    vpn_data = cursor.fetchone()
                    # print(vpn_data)

                    cursor.execute("SELECT ID,Info FROM Info WHERE Function_Code=?", (pro_code,))
                    web_info = cursor.fetchone()

                    # com_name,pro_name,VPN_addr,VPN_user,VPN_pwd,web_name,web_addr,web_info = com_name,pro_name,vpn_data[0],vpn_data[1],vpn_data[2],web_name, web_addr, web_info
                    com_id, com_name, pro_id, pro_name, VPN_id, VPN_addr, VPN_user, VPN_pwd, web_name_id, web_name, web_addr_id, web_addr, web_info_id, web_info = com_id, com_name, pro_id, pro_name, \
                        vpn_data[0], vpn_data[1], vpn_data[2], vpn_data[3], web_name_id, web_name, web_addr[0], \
                    web_addr[1], web_info[0], web_info[1]
                    my_dict.update(
                        {'公司名称ID': com_id, '公司名称': com_name, '项目名称ID': pro_id, '项目名称': pro_name,
                         'VPNID': VPN_id, 'VPN地址': VPN_addr,
                         'VPN用户名': VPN_user, 'VPN密码': VPN_pwd,
                         '子项目名称ID': web_name_id, '子项目名称': web_name,
                         '子项目路径ID': web_addr_id, '子项目路径': web_addr, '项目信息ID': web_info_id,
                         '项目信息': web_info})

                    # print("my_dict=", my_dict)
                    list_assistant.append(copy.deepcopy(my_dict))
                    # print("list_assistant=", list_assistant)
        # print("my_dict=",self.my_dict)
        # print("list_assistant=", list_assistant)
        # print(data1)
        # print(self.companies)
        return list_assistant

    # 保存新数据或更新数据到数据库的函数
    def save_data(self):
        # row_entries = []  # 用一个字典来保存这一行的所有输入框，便于后续保存数据
        # # 用来保存输入框的列表
        # entries = []
        # print(self.entry.get())
        # row_entries.append(self.entry.get())  # 保存输入框
        # entries.append(row_entries)
        # print(self.entries)
        entries2 = []

        new_entries = [self.entries[i:i + 14] for i in range(0, len(self.entries), 14)]

        for i in range(0, len(new_entries)):
            values = []
            for self.entry in new_entries[i]:
                # print(self.entry)
                # row_entries = []  # 用一个字典来保存这一行的所有输入框，便于后续保存数据
                value = self.entry.get()
                # print(value)
                # row_entries.append(value)
                values.append(value)
                entries2.append(values)
            # print(values)
            i += 1

        # conn = sqlite3.connect('gui.db')
        # cursor = conn.cursor()
        # print("'{}'".format self.entries)
        # current_time = datetime.datetime.now()
        # current_time = datetime.datetime.now().isoformat()
        # print(current_time)

        # print(entries2)
        try:
            # print('info_data=', info_data)
            # print('info_entry=', entry[12], entry[13])
            # 遍历条目并更新数据库
            for entry in entries2:
                # print((entry[1]))
                cursor.execute(
                    "select ID , Function_Name from  Function  WHERE ID=? ",
                    ((entry[0]),))
                com_data = cursor.fetchone()
                # print('com_data=',com_data)
                # print('com_entry=', entry[0],entry[1])
                cursor.execute(
                    "select ID , Function_Name from  Function  WHERE ID=? ",
                    ((entry[2]),))
                pro_data = cursor.fetchone()
                # print('pro_data=', pro_data)
                # print('entry_data=', entry[2], entry[3])
                cursor.execute(
                    "select ID ,Function_Url ,Function_User,Function_Password  from  Function_Users  WHERE ID=? ",
                    ((entry[4]),))
                vpn_data = cursor.fetchone()
                # print('vpn_data=', vpn_data)
                # print('vpn_entry=', entry[4], entry[5], entry[6], entry[7])
                cursor.execute(
                    "select ID , Function_Name from  Function  WHERE ID=? ",
                    ((entry[8]),))
                web_data = cursor.fetchone()
                # print(pro_data)
                cursor.execute(
                    "select ID , Tools_Path from  Tools  WHERE ID=? ",
                    ((entry[10]),))
                tool_data = cursor.fetchone()
                # print(tool_data)
                cursor.execute(
                    "select ID , Info from  Info  WHERE ID=? ",
                    ((entry[12]),))
                info_data = cursor.fetchone()

                # 假设 'entries' 是一个字典列表或类似的结构
                # 根据你的架构和数据结构调整SQL和数据提取逻辑

                if com_data[0] == entry[0] and com_data[1] == entry[1]:
                    pass
                    # print('com_data=', com_data)
                    # print('com_entry=', entry[0], entry[1])
                else:
                    cursor.execute(
                        "UPDATE Function SET Function_Name=? ,Updata_Time=datetime() WHERE ID=?",
                        ((entry[1]), (entry[0])))
                    # conn.commit()
                    # print(1)

                if pro_data[0] == entry[2] and pro_data[1] == entry[3]:
                    pass
                else:
                    cursor.execute(
                        "UPDATE Function SET Function_Name=? ,Updata_Time=datetime()  WHERE ID=?",
                        ((entry[3]), (entry[2])))
                    # conn.commit()
                    # print(2)

                if vpn_data[0] == entry[4] and vpn_data[1] == entry[5] and vpn_data[2] == entry[6] and vpn_data[3] == \
                        entry[7]:
                    pass
                else:
                    cursor.execute(
                        "UPDATE Function_Users SET Function_Url=? ,Function_User=?,Function_Password = ? ,Updata_Time=datetime() WHERE ID=?",
                        ((entry[5]), (entry[6]), (entry[7]), (entry[4])))
                    # conn.commit()
                    # print(3)

                if web_data[0] == entry[8] and web_data[1] == entry[9]:
                    pass
                else:
                    cursor.execute(
                        "UPDATE Function SET Function_Name=? ,Updata_Time=datetime()  WHERE ID=?",
                        ((entry[9]), (entry[8])))
                    # conn.commit()
                    # print(4)

                if tool_data[0] == entry[10] and tool_data[1] == entry[11]:
                    pass
                else:
                    cursor.execute(
                        "UPDATE Tools SET Tools_Path=? ,Updata_Time=datetime()  WHERE ID=?",
                        ((entry[11]), (entry[10])))
                    # conn.commit()
                    # print(5)

                if info_data[0] == entry[12] and info_data[1] == entry[13]:
                    pass
                else:
                    cursor.execute(
                        "UPDATE Info SET Info=? ,Updata_Time=datetime()  WHERE ID=?",
                        ((entry[13]), (entry[12])))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating Function table: {e}")
            # print(6)
            # entry['公司名称'], entry['项目名称'], entry['VPN地址'], entry['VPN用户名'], entry['VPN密码'],entry['子项目名称'], entry['子项目路径'], entry['项目信息'], entry['id']

        # 关闭维护窗口并刷新主应用视图
        self.maintain_window.destroy()
        self.refresh_main_view()

    # def get_values(self):
    #     # print(self.entries)
    #     new_entries = [self.entries[i:i + 14] for i in range(0, len(self.entries), 14)]
    #     for i in range(0,len(new_entries)):
    #         values = []
    #         for self.entry in new_entries[i]:
    #             # print(self.entry)
    #             # row_entries = []  # 用一个字典来保存这一行的所有输入框，便于后续保存数据
    #             value = self.entry.get()
    #             # print(value)
    #             # row_entries.append(value)
    #             values.append(value)
    #         # print(values)
    #     i+=1

    # 刷新主应用视图的函数（你需要根据你的应用定义这个函数）
    def refresh_main_view(self):
        # 刷新主应用的显示代码
        # 读取公司数据
        self.companies = {}

        cursor.execute("SELECT Function_Name, Function_Code FROM function WHERE Function__Level='2'")
        com_names = cursor.fetchall()

        for com_name, com_code in com_names:
            cursor.execute(
                "SELECT Function_Name, Function_Code FROM function WHERE Function__Superior=? AND Function__Level='3'",
                (com_code,))
            pro_names = cursor.fetchall()

            for pro_name, pro_code in pro_names:
                cursor.execute(
                    "SELECT Function_Name, Function_Code FROM function WHERE Function__Superior=? AND Function__Level='4'",
                    (pro_code,))
                web_names = cursor.fetchall()

                for web_name, web_code in web_names:
                    cursor.execute("SELECT Tools_Path FROM Tools WHERE Function_Code=?", (web_code,))
                    web_addr = cursor.fetchone()[0]

                    cursor.execute(
                        "SELECT Function_Url, Function_User, Function_Password FROM Function_Users WHERE Function_Code=?",
                        (pro_code,))
                    vpn_data = cursor.fetchone()

                    cursor.execute("SELECT Info FROM Info WHERE Function_Code=?", (pro_code,))
                    web_info = cursor.fetchone()[0]

                    com_name, pro_name, VPN_addr, VPN_user, VPN_pwd, web_name, web_addr, web_info = com_name, pro_name, \
                        vpn_data[0], vpn_data[1], vpn_data[2], web_name, web_addr, web_info
                    self.companies[web_name, web_addr] = (com_name, pro_name, VPN_addr, VPN_user, VPN_pwd, web_info)
                    # print((com_name, pro_name, VPN_addr, VPN_user, VPN_pwd, web_info))
        # self.create_widgets()
        self.display_homepage()

    # 处理 "维护信息" 操作的函数
    def maintain_information(self):
        data = self.fetch_current_data()
        # print(data)
        # print(len(data))
        self.maintain_window = Toplevel(root)
        self.maintain_window.title("维护信息")
        self.maintain_window.geometry(f"1370x460")

        # 创建一个滚动条
        scroll_bar = tk.Scrollbar(self.maintain_window, borderwidth=20, width=19)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.BOTH)
        scroll_bar2 = tk.Scrollbar(self.maintain_window, orient=HORIZONTAL, borderwidth=20, width=19)
        scroll_bar2.pack(side=tk.BOTTOM, fill=tk.BOTH)

        # 创建一个Canvas，并与滚动条绑定
        canvas = tk.Canvas(self.maintain_window, yscrollcommand=scroll_bar.set, xscrollcommand=scroll_bar2.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_bar.config(command=canvas.yview)
        scroll_bar2.config(command=canvas.xview)

        # 创建一个frame放在Canvas内
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        # # 用来保存输入框的列表
        self.entries = []

        # 动态创建标签和输入框来显示每条数据
        for i in range(0, len(data)):
            # row_entries = []  # 用一个字典来保存这一行的所有输入框，便于后续保存数据
            for index, (key, row) in enumerate(data[i].items()):
                # print("i=", i)
                # print("index=", index)
                # print("key=", key)
                # print("row=", row)
                # 创建标签
                #     tk.Label(frame, text=f"          {key}{i + 1}           ").grid(row= 2 * i, column=index, sticky="e")
                tk.Label(frame, text=key).grid(row=0, column=index, sticky="ew")
                # 创建输入框，初始化为当前数据
                self.entry = tk.Entry(frame, xscrollcommand=20)
                self.entry.insert(0, row)
                self.entry.grid(row=2 * i + 1, column=index)
                if 'ID' in key:
                    self.entry.config(state='readonly')  # 或者使用 state=tk.DISABLED
                # 保存按钮
                save_button = tk.Button(frame, text="   保存   ", command=lambda: self.save_data())
                # row = 2 * len(data) - 1
                # column = index + 2
                # print(row)
                save_button.grid(row=2 * i + 1, column=20)

                # print(self.entry.get())
                # row_entries.append(self.entry.get())  # 保存输入框
                self.entries.append(self.entry)
            i += 1

        # print("row_entries=",row_entries)
        # self.entries.append(row_entries)
        # print("entries=",self.entries)

        # # 保存按钮
        # save_button = tk.Button(frame, text="   保存   ", command=lambda: self.get_entry_values())
        # row = 2 * len(data) - 1
        # column = index + 2
        # # print(row)
        # save_button.grid(row=row, column=column)

        # 更新canvas的滚动区域
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        self.maintain_window.mainloop()

    def create_add_data_form(self):
        self.add_data_window = Toplevel(self.master)
        self.add_data_window.title("增加信息")
        self.add_data_window.geometry(f"300x410")

        # Labels and Entry Widgets for each field
        labels = ["公司名称", "项目名称", "VPN 地址", "VPN 用户", "VPN 密码", "名称",
                  "地址", "说明"]
        self.entries = {}
        for i, label in enumerate(labels):
            Label(self.add_data_window, text=label).grid(row=i, column=0, sticky="ew", padx=10, pady=10)
            entry = Entry(self.add_data_window)
            entry.grid(row=i, column=1, sticky="ew", padx=10, pady=10)
            self.entries[label] = entry

        # Save Button
        ttk.Button(self.add_data_window, text="保存", command=self.submit_data).grid(row=len(labels), columnspan=2,
                                                                                     sticky="ew", padx=15, pady=10)

    def submit_data(self):
        # 从输入框收集数据
        data = {label: entry.get() for label, entry in self.entries.items()}
        # print(data)

        try:
            # 检查并插入公司名称
            self.check_and_insert_com_name_code(data["公司名称"], 2, None)

            # 检查并插入项目名称
            com_name_code = self.get_function_code_com_name_code(data["公司名称"])
            self.check_and_insert_project_name_code(data["项目名称"], 3, com_name_code)

            # 检查并插入名称
            project_name_code = self.get_function_code_project_name_code(data["项目名称"])
            self.check_and_insert_pro_name_code(data["名称"], 4, project_name_code)

            # 检查并插入说明
            project_name_code = self.get_function_code_project_name_code(data["项目名称"])
            self.check_and_insert_info_name_code(data["说明"], project_name_code)

            # 检查并插入VPN
            project_name_code = self.get_function_code_project_name_code(data["项目名称"])
            self.check_and_insert_vpn_name_code(data["VPN 地址"], data["VPN 用户"], data["VPN 密码"], project_name_code)

            # 检查并插入路径
            pro_name_code = self.get_function_code_pro_name_code(data["名称"])
            self.check_and_insert_addr_name_code(data["名称"], data["地址"], pro_name_code)

            conn.commit()
        except Exception as e:
            print("发生错误:", e)
            conn.rollback()  # 回滚在异常时的任何数据库操作

        self.add_data_window.destroy()
        self.refresh_main_view()

    def check_and_insert_com_name_code(self, name, level, superior_code):
        # 生成随机ID和当前时间
        random_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        """检查名称是否存在并插入新记录"""
        cursor.execute("SELECT Function_Code FROM function WHERE Function_Name=?", (name,))
        result = cursor.fetchone()
        if not result:
            cursor.execute(
                "INSERT INTO Function (ID,Function_Code, Function_Name,Function__Level,Function__Superior) "
                "VALUES (?,?,?,?,?)",
                (random_id, random_id, name, level, superior_code))

    def check_and_insert_project_name_code(self, name, level, superior_code):
        # 生成随机ID和当前时间
        random_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        """检查名称是否存在并插入新记录"""
        cursor.execute("SELECT Function_Code FROM function WHERE Function_Name=? and Function_Code=?",
                       (name, superior_code))
        result = cursor.fetchone()
        if not result:
            cursor.execute(
                "INSERT INTO Function (ID,Function_Code, Function_Name,Function__Level,Function__Superior) "
                "VALUES (?,?,?,?,?)",
                (random_id, random_id, name, level, superior_code))

    def check_and_insert_pro_name_code(self, name, level, superior_code):
        # 生成随机ID和当前时间
        random_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        """检查名称是否存在并插入新记录"""
        cursor.execute("SELECT Function_Code FROM function WHERE Function_Name=? and Function_Code=?",
                       (name, superior_code))
        result = cursor.fetchone()
        if not result:
            cursor.execute(
                "INSERT INTO Function (ID,Function_Code, Function_Name,Function__Level,Function__Superior) "
                "VALUES (?,?,?,?,?)",
                (random_id, random_id, name, level, superior_code))

    def check_and_insert_info_name_code(self, name, superior_code):
        # 生成随机ID和当前时间
        random_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        """检查名称是否存在并插入新记录"""
        cursor.execute("SELECT Function_Code FROM function WHERE Function_Name=? and Function_Code=?",
                       (name, superior_code))
        result = cursor.fetchone()
        if not result:
            cursor.execute(
                "INSERT INTO info (ID,info_Code, info,Function_Code) "
                "VALUES (?,?,?,?)",
                (random_id, random_id, name, superior_code))

    def check_and_insert_vpn_name_code(self, addr, user, passwd, superior_code):
        # 生成随机ID和当前时间
        random_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        """检查名称是否存在并插入新记录"""
        cursor.execute(
            "SELECT ID FROM Function_Users WHERE Function_Url=? and Function_User=? and Function_Password=? and Function_Code=?",
            (addr, user, passwd, superior_code))
        result = cursor.fetchone()
        if not result:
            cursor.execute(
                "INSERT INTO Function_Users (ID,Function_Url,Function_User, Function_Password,Function_Code) "
                "VALUES (?,?,?,?,?)",
                (random_id, addr, user, passwd, superior_code))

    def check_and_insert_addr_name_code(self, name1, name2, superior_code):
        # 生成随机ID和当前时间
        random_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        """检查名称是否存在并插入新记录"""
        cursor.execute("SELECT Tools_Code FROM Tools WHERE Tools_Name=? and Function_Code = ?", (name1, superior_code))
        result = cursor.fetchone()
        if not result:
            cursor.execute(
                "INSERT INTO Tools (ID,Tools_Code, Tools_Name,Tools_Path,Function_Code) "
                "VALUES (?,?,?,?,?)",
                (random_id, random_id, name1, name2, superior_code,))

    def get_function_code_com_name_code(self, name):
        """获取特定名称的功能代码"""
        cursor.execute("SELECT Function_Code FROM function WHERE Function_Name=?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_function_code_project_name_code(self, name):
        """获取特定名称的功能代码"""
        cursor.execute("SELECT Function_Code FROM function WHERE Function_Name=?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_function_code_pro_name_code(self, name):
        """获取特定名称的功能代码"""
        cursor.execute("SELECT Function_Code FROM function WHERE Function_Name=?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def display_company(self, name):
        # 清空页面框架
        for widget in self.page_frame.winfo_children():
            widget.destroy()

        self.text.destroy()
        self.save_btn.destroy()
        self.time_label.destroy()
        # 显示公司项目
        list2 = []
        for (web_name, web_addr), (
                com_name, pro_name, VPN_addr, VPN_user, VPN_pwd, web_info) in self.companies.items():
            details2 = com_name, pro_name
            list2.append(details2)

        set2 = set(list2)
        set22 = sorted(set2)

        # print(set22)
        ttk.Label(self.page_frame, text=name).grid(row=0, column=0)

        lll = 0
        row = 1
        for lll in range(len([item[0] for item in set22])):
            if name == [item[0] for item in set22][lll]:
                # print(name)
                # print([item[0] for item in set22][lll])
                # print([item[1] for item in set22][lll])
                b1 = ttk.Button(self.page_frame, text=[item[1] for item in set22][lll],
                                command=lambda pn=[item[1] for item in set22][lll]: self.display_project(name, pn))
                b1.grid(row=row, column=0, sticky="ew", padx=10, pady=10)
                row += 1
            lll += 1

        # 返回首页按钮
        ttk.Button(self.page_frame, text="返回首页", command=self.display_homepage).grid(row=row, column=0, sticky="ew",
                                                                                         padx=10, pady=10)

        # 当前时间
        self.time_label = ttk.Label(self.master, textvariable=self.time_var)
        self.time_label.place(relx=0.5, rely=0.99, anchor='center')

    def display_project(self, company, project):
        # 清空页面框架
        for widget in self.page_frame.winfo_children():
            widget.destroy()
        self.time_label.destroy()
        ttk.Label(self.page_frame, text=company).grid(row=0, column=0)
        ttk.Label(self.page_frame, text=project).grid(row=0, column=1)

        # 读取之前保存的text内容
        cursor.execute(
            "SELECT Info FROM Info WHERE Function_Code= (select Function_Code from Function where Function_name = ?)",
            (project,))
        web_info = cursor.fetchone()[0]
        saved_text = web_info

        # 创建text组件
        self.text = tk.Text(self.master, width=50, height=30)
        self.text.pack(side=tk.LEFT)
        # 保存按钮
        self.save_btn = ttk.Button(self.master, text='保存',
                                   command=lambda: self.save_text(company, project))
        self.save_btn.pack(side=tk.LEFT)

        self.text.delete("1.0", tk.END)

        # 插入之前的内容
        if saved_text:
            self.text.insert('1.0', saved_text)

        list3 = []
        for (web_name, web_addr), (
                com_name, pro_name, VPN_addr, VPN_user, VPN_pwd, web_info) in self.companies.items():
            details3 = com_name, pro_name, web_name, web_addr, web_info
            list3.append(details3)

        set3 = set(list3)
        set33 = sorted(set3)

        # 使公司框架列自动扩展
        self.page_frame.grid_columnconfigure(0, weight=1)
        self.page_frame.grid_columnconfigure(1, weight=1)
        # print(company,project)
        kkk = 0
        listlll = []
        listlll2 = []
        for kkk in range(len([item[0] for item in set33])):
            if company == [item[0] for item in set33][kkk] and project == [item[1] for item in set33][kkk]:
                # 计算按钮数
                listlll.append([item[2] for item in set33][kkk])
                listlll2.append([item[3] for item in set33][kkk])
                num_buttons = len(listlll)
                cols = num_buttons // 3 + 1
            kkk += 1

        # 循环创建按钮
        for ooo in range(num_buttons):
            # 计算按钮位置
            row = ooo // cols
            col = ooo % cols
            website_name = listlll[ooo]
            website_url = listlll2[ooo]
            b1 = ttk.Button(self.page_frame, text=website_name,
                            command=lambda url=website_url: self.open_website(url))
            b1.grid(row=col + 1, column=row, sticky="nsew", padx=10, pady=10)

        # 返回上级界面
        back_bt = ttk.Button(self.page_frame, text="返回上级界面",
                             command=lambda: self.display_company(company)).grid(row=cols + 1, column=2, sticky="nsew",
                                                                                 padx=10, pady=10)
        self.vpn_bt = ttk.Button(self.page_frame, text="登录VPN",
                                 command=lambda: connect_vpn(company + project)).grid(row=cols + 1, column=0,
                                                                                      sticky="nsew", padx=10, pady=10)

        self.vpnquit_bt = ttk.Button(self.page_frame, text="退出VPN", command=lambda: self.VPN_EXIT()).grid(
            row=cols + 1, column=1, sticky="nsew", padx=10, pady=10)

        # 当前时间
        self.time_label = ttk.Label(self.master, textvariable=self.time_var)
        self.time_label.place(relx=0.5, rely=0.99, anchor='center')

    # 保存函数
    def save_text(self, company, project):
        # 获取self.text内容
        text_content = self.text.get('1.0', 'end')
        # 读取之前保存的text内容
        web_info = text_content
        print(web_info)
        cursor.execute(
            "update Info set info =? where Function_Code= (select Function_Code from Function where Function_name = ?)",
            (web_info, project))
        conn.commit()

    def select_bg_image(self):
        filename = tk.filedialog.askopenfilename(title="选择背景图片", filetypes=[(".png files", ".png")])
        if filename:
            self.bg_image = ImageTk.PhotoImage(Image.open(filename))
            self.bg_label.configure(image=self.bg_image)
            Image.open(filename).save('bg.png')
            GUI_w2, GUI_h2 = Image.open(filename).size
            self.master.geometry(f"{GUI_w2}x{GUI_h2}")

    def open_url(self):
        webbrowser.open("http://muerfeng.top")

    def select_sys_clean(self):
        os.system('../缓存清理.bat')

    def select_net_clean(self):
        os.system('../网络重置.bat')

    def open_website(self, url):
        print(url)
        with open("OpenUrl.bat", "w") as f:
            f.write(f"start {url}\n")
        os.system("OpenUrl.bat")

    def quit(self):
        if messagebox.askokcancel("退出", "确定要退出吗?"):
            self.master.destroy()

    def VPN_EXIT(self):
        # 判断VPN程序是否正在运行
        process_name = ["EasyConnect.exe", "SangforCSClient.exe", "SangforCSClient.exe"]
        for proc in psutil.process_iter():
            try:
                process_info = proc.as_dict(attrs=['pid', 'name'])
                # 如果VPN程序已打开，杀死程序
                if process_info['name'] in process_name:
                    proc.terminate()
            except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                print("未发现EasyConnect程序")

    def refresh(self):
        # 获取完整时间信息
        current_time = time.localtime()

        year = current_time.tm_year
        month = current_time.tm_mon
        day = current_time.tm_mday
        hour = current_time.tm_hour
        minute = current_time.tm_min
        second = current_time.tm_sec

        lunar_date = LunarDate.fromSolarDate(year, month, day)

        lunar_year = lunar_date.year
        lunar_month = lunar_date.month
        lunar_day = lunar_date.day
        # 转换为农历
        if lunar_day <= 10:
            time_str = f'{year}年{month}月{day}日{hour}:{minute}:{second}        农历{lunar_year}年{lunar_month}月初{lunar_day}'
        else:
            time_str = f'{year}年{month}月{day}日{hour}:{minute}:{second}        农历{lunar_year}年{lunar_month}月{lunar_day}'

        self.time_var.set(time_str)
        self.master.after(1000, self.refresh)


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginGUI(root)
    app.refresh()
    root.mainloop()