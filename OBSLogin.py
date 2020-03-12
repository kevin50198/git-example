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
element = driver.find_element_by_id("loginbutton").click()

element = driver.find_element_by_id("accountId")
element.send_keys("F62127")

element = driver.find_element_by_name("accountPwd")
element.send_keys("qaz123")

element = driver.find_element_by_id("signin").click()
