# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re , os , time ,random ,string

#打開網頁,最大化瀏覽器
driver = webdriver.Chrome()
driver.get("https://ku112.net/")
driver.maximize_window()

#找到輸入框->輸入內容
driver.find_element_by_id("loginbutton").click()

element = driver.find_element_by_id("accountId")
element.send_keys("F62127")

element = driver.find_element_by_name("accountPwd")
element.send_keys("qaz123")

driver.find_element_by_id("signin")
time.sleep(5)

def tryclick(count=0): ##保護機制，以防無法定位到還沒渲染出來的元素
    try:
        element = driver.find_element_by_id("signin")
        # elem = driver.find_element_by_xpath(Xpath)  # 如果你想透過Xpath定位元素
        element.click() # 點擊定位到的元素
    except:
        time.sleep(2)
        count+=1
        if(count <2):
            tryclick(count)
        else:
            print("cannot locate element")
tryclick()

#time.sleep(3) # 等待javascript渲染出來，當然這個部分還有更進階的作法，關鍵字是implicit wait, explicit wait，有興趣可以自己去找
#html = driver.page_source # 取得html文字
#driver.close()  # 關掉Driver打開的瀏覽器
#print(html)

#driver.find_element_by_xpath("//*[@id='menu_personal_maintain_bblive']/a").click()
#time.sleep(1)
#driver.find_element_by_xpath("//*[@id='FastTransfer']/form/div[2]/div/div/input[1]").click()
