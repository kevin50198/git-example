# coding:utf-8
from selenium import webdriver
from PIL import Image , ImageEnhance
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract , re , requests , os , time ,random ,string
#打開網頁,最大化瀏覽器
driver = webdriver.Chrome()
driver.get("http://ctl.memlottery.org/")
driver.implicitly_wait(10)
driver.maximize_window()

#找到輸入框->輸入內容
element = driver.find_element_by_id("acc")
element.send_keys("kevin50198")

element = driver.find_element_by_id("pwd")
element.send_keys("z1x2c3v4b5")

#手動key OTP時間
element = driver.find_element_by_id("ga_code").click()
time.sleep(3)

#提交表單
element = driver.find_element_by_id("btn_login")
element.click()

try:
	#確定alert
	time.sleep(1)
	driver.switch_to.alert.accept()
except:
	time.sleep(1)

#關閉稽核彈窗
time.sleep(1)
driver.find_element_by_css_selector("[class='icon-close ZwClose']").click()

#點擊代理商管理->期數管理->alert
time.sleep(1)
driver.find_element_by_css_selector("[class='fa fa-bookmark-o']").click()

time.sleep(1)
element = driver.find_element_by_id("agents.issue_view.list").click()

#選擇周期
time.sleep(1)
element = Select(driver.find_element_by_id("days"))
element.select_by_index(1)

#抓取所有期數
element = driver.find_element_by_css_selector("[class='ui-jqgrid ui-widget ui-widget-content ui-corner-all']")
print(element.text)