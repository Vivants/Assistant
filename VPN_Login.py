import time
import psutil
import os
import sys
from selenium import webdriver
import openpyxl
import sqlite3

# 连接数据库
conn = sqlite3.connect('gui.db')
cursor = conn.cursor()

class VPN:
    def __init__(self):
        # VPN信息文件所在位置
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

                    com_name,pro_name,VPN_addr,VPN_user,VPN_pwd = com_name,pro_name,vpn_data[0],vpn_data[1],vpn_data[2]
                    self.companies[com_name, pro_name] = (VPN_addr, VPN_user, VPN_pwd)

        # print(self.companies)

    def EasyConnect(self):
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

    def EasyConnect2(self):
        # 判断VPN程序是否已正常启动
        process_name = "EasyConnect.exe"
        for proc in psutil.process_iter():
            process_info = proc.as_dict(attrs=['pid', 'name'])
            if process_info['name'] == process_name:
                return 1

    def Chrome(self):
        list3 = []
        for (com_name, pro_name), (
                 VPN_addr, VPN_user, VPN_pwd) in self.companies.items():
            details3 = com_name, pro_name,VPN_addr, VPN_user, VPN_pwd
            list3.append(details3)

        set3 = set(list3)
        set33 = sorted(set3)

        # print(company,project)
        for kkk in range(len([item[0] for item in set33])):
            if self.TYPE == [item[0] for item in set33][kkk] + [item[1] for item in set33][kkk]:
                # 计算按钮数
                VPN_addr = ([item[2] for item in set33][kkk])
                VPN_user = ([item[3] for item in set33][kkk])
                VPN_pwd = ([item[4] for item in set33][kkk])
        # 进行浏览器登录操作（仅限Chrome浏览器），适用于新版本VPN程序
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(VPN_addr)
        login_button = self.driver.find_element("id", "details-button")
        login_button.click()
        login_button = self.driver.find_element("id", "proceed-link")
        login_button.click()
        time.sleep(3)
        username_input = self.driver.find_element("class name", "input-txt")
        password_input = self.driver.find_element("id", "loginPwd")
        time.sleep(0.5)
        username_input.send_keys(VPN_user)
        time.sleep(0.5)
        password_input.send_keys(VPN_pwd)
        login_button = self.driver.find_element("class name", "checkbox--small")
        login_button.click()
        login_button = self.driver.find_element("class name", "button__text")
        login_button.click()


    def Chrome_Old(self):
        list3 = []
        for (com_name, pro_name), (
                 VPN_addr, VPN_user, VPN_pwd) in self.companies.items():
            details3 = com_name, pro_name,VPN_addr, VPN_user, VPN_pwd
            list3.append(details3)

        set3 = set(list3)
        set33 = sorted(set3)

        # print(company,project)
        for kkk in range(len([item[0] for item in set33])):
            if self.TYPE == [item[0] for item in set33][kkk] + [item[1] for item in set33][kkk]:
                # 计算按钮数
                VPN_addr = ([item[2] for item in set33][kkk])
                VPN_user = ([item[3] for item in set33][kkk])
                VPN_pwd = ([item[4] for item in set33][kkk])
        # 进行浏览器登录操作（仅限Chrome浏览器），适用于旧版本VPN程序
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(VPN_addr)
        login_button = self.driver.find_element("id", "details-button")
        login_button.click()
        login_button = self.driver.find_element("id", "proceed-link")
        login_button.click()
        time.sleep(3)
        username_input = self.driver.find_element("id", "svpn_name")
        password_input = self.driver.find_element("id", "svpn_password")
        time.sleep(0.5)
        username_input.send_keys(VPN_user)
        time.sleep(0.5)
        password_input.send_keys(VPN_pwd)
        # login_button = self.driver.find_element("class name", "checkbox--small")
        # login_button.click()
        login_button = self.driver.find_element("id", "logButton")
        login_button.click()

    def Bat(self):
        while True:
            if self.EasyConnect2() == 1:
                # print("VPN登陆成功")
                self.driver.quit
                break
            else:
                time.sleep(1)

    def run(self, company):
        # print(company)
        if company == '浪潮集团工作':
            #inspur VPN版本较低，网页按钮不同
            self.TYPE = company
            self.EasyConnect()
            self.Chrome_Old()
            self.EasyConnect2()
            self.Bat()
        # 再有不同VPN版本的在这里添加
        # elif company == '':
        #     pass
        else:
            self.TYPE = company
            self.EasyConnect()
            self.Chrome()
            self.EasyConnect2()
            self.Bat()



# vpn = VPN()
# vpn.run('山西国有资本运营有限公司数据中台')