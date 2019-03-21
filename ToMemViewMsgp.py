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
driver.get("http://ctl.glassshoes.info/")
driver.implicitly_wait(10)
driver.maximize_window()

#找到輸入框->輸入內容
element = driver.find_element_by_id("acc")
element.send_keys("kevin50198")

element = driver.find_element_by_id("pwd")
element.send_keys("z1x2c3v4b5")

element = driver.find_element_by_id("ga_code")
element.send_keys("1")

#提交表單
element = driver.find_element_by_id("btn_login")
element.click()

#確定alert
time.sleep(1)
driver.switch_to.alert.accept()

#關閉稽核彈窗
time.sleep(1)
driver.find_element_by_css_selector("[class='icon-close ZwClose']").click()

#點擊網站管理->一般站內信->新增
time.sleep(1)
driver.find_element_by_css_selector("[class='fa fa-sitemap']").click()

time.sleep(1)
element = driver.find_element_by_id("misc.mnews_view.list")
element.click()

time.sleep(1)
driver.find_element_by_css_selector("[class='btns btns-blue btn_ctl btn_add']").click()

#找到單個iframe->輸入帳號/標題
time.sleep(1)
driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))

element = driver.find_element_by_id("acc")
element.send_keys("stan168")

element = driver.find_element_by_id("subject")
element.send_keys("auto send")

#內容有另一個iframe
driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
element = driver.find_element_by_css_selector("[class='ke-content']")
element.send_keys("發起來")

#回上一層frame按確定
driver.switch_to.parent_frame()  #回上一層frame
element = driver.find_element_by_id("btn_add_f")
element.click();

#確定alert
time.sleep(1)
driver.switch_to.alert.accept()