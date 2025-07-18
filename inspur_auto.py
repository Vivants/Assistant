import time
from selenium import webdriver
import keyboard
import pyautogui
import random

# 进行浏览器登录操作（仅限Chrome浏览器）
options = webdriver.ChromeOptions()

options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)

driver.get("https://office.inspur.com/")

time.sleep(5)

username_input = driver.find_element("css selector", "#adminLoginform > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(1) > td.bj01.login_nyjtd.fill_in_text > input[type=text]")

password_input = driver.find_element("css selector", "#adminLoginform > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(3) > td.bj02.login_nyjtd.fill_in_text > input[type=password]")

time.sleep(0.5)

username_input.send_keys("用户名")

time.sleep(0.5)

password_input.send_keys("密码")

time.sleep(0.5)

login_button = driver.find_element("css selector", "#adminLoginform > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(1) > button")

login_button.click()

time.sleep(8)

# Get the position of the specific location on the screen
# time.sleep(3)
# position = pyautogui.position()
# print(position)
# 集团新闻
position = [357, 501]

i = 0

for i in range(10):

    # Click on the specific location
    pyautogui.click(position[0], position[1])
    time.sleep(1)
    pyautogui.scroll(-300)
    time.sleep(1)
    pyautogui.scroll(-300)
    time.sleep(1)
    pyautogui.scroll(-300)
    time.sleep(random.randint(20, 30))
    keyboard.press('ctrl')
    keyboard.press('w')
    keyboard.release('w')
    keyboard.release('ctrl')
    time.sleep(1)
    i += 1
    position[1] += 30
#     print(position)

# 集团公告
time.sleep(3)
pyautogui.scroll(-800)
# position = pyautogui.position()
# print(position)
position2 = [357, 501]

l = 0

for l in range(10):

    # Click on the specific location
    pyautogui.click(position2[0], position2[1])
    time.sleep(1)
    pyautogui.scroll(-300)
    time.sleep(1)
    pyautogui.scroll(-300)
    time.sleep(1)
    pyautogui.scroll(-300)
    time.sleep(random.randint(20, 30))
    keyboard.press('ctrl')
    keyboard.press('w')
    keyboard.release('w')
    keyboard.release('ctrl')
    time.sleep(1)
    l += 1
    position2[1] += 30
    # print(position2)

# 专题新闻
time.sleep(3)
pyautogui.scroll(800)
pyautogui.press('right')
pyautogui.press('right')
pyautogui.press('right')
pyautogui.press('right')
pyautogui.press('right')
pyautogui.press('right')
pyautogui.press('right')
pyautogui.press('right')

# 党群动态
time.sleep(3)
position3 = [673, 501]

ii = 0

for ii in range(10):

    # Click on the specific location
    pyautogui.click(position3[0], position3[1])
    time.sleep(1)
    pyautogui.scroll(-300)
    time.sleep(1)
    pyautogui.scroll(-300)
    time.sleep(1)
    pyautogui.scroll(-300)
    time.sleep(random.randint(20, 30))
    keyboard.press('ctrl')
    keyboard.press('w')
    keyboard.release('w')
    keyboard.release('ctrl')
    time.sleep(1)
    ii += 1
    position3[1] += 30
    # print(position2)
#
time.sleep(3)
pyautogui.scroll(-800)
position4 = [673, 501]

ll = 0

for ll in range(10):

    # Click on the specific location
    pyautogui.click(position4[0], position4[1])
    time.sleep(1)
    pyautogui.scroll(-300)
    time.sleep(1)
    pyautogui.scroll(-300)
    time.sleep(1)
    pyautogui.scroll(-300)
    time.sleep(random.randint(20, 30))
    keyboard.press('ctrl')
    keyboard.press('w')
    keyboard.release('w')
    keyboard.release('ctrl')
    time.sleep(1)
    ll += 1
    position4[1] += 30
    # print(position2)