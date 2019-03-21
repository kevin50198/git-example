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
element.click();

#確定alert
WebDriverWait(driver,10).until(EC.alert_is_present())
driver.switch_to.alert.accept()

#關閉稽核彈窗
time.sleep(1)
driver.find_element_by_css_selector("[class='icon-close ZwClose']").click()

#點擊會員管理->會員資料->新增
time.sleep(1)
driver.find_element_by_css_selector("[class='fa fa-user']").click()

time.sleep(1)
element = driver.find_element_by_id("members.mem_view.list")
element.click()

def mem_add():
	time.sleep(1)
	driver.find_element_by_css_selector("[class='icon-circle-plus']").click()

	#找到單個iframe->輸入帳號/密碼/代理
	time.sleep(1)
	driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))

	#帳號隨機產生 3 個字元組合的 0-9 中任一字元
	element = driver.find_element_by_id("acc")
	element.send_keys('stan' +''.join(random.choice(string.digits) for x in range(3)))

	# 隨機產生 a-z / A-Z 中任一字元
	# random.choice(string.ascii_letters)

	# 隨機產生 0-9 中任一字元
	# random.choice(string.digits)

	# 隨機產生 10 個字元組合的 a-z / A-Z 中任一字元
	# ''.join(random.choice(string.ascii_letters) for x in range(10))

	# 隨機產生 10 個字元組合的 0-9 中任一字元
	# ''.join(random.choice(string.digits) for x in range(10))

	# 帳號隨機產生 10 個字元組合，包含 0-9, a-z, A-Z 中任一字元
	# ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10)))

	element = driver.find_element_by_id("pwd")
	element.send_keys("stan168")

	element = driver.find_element_by_id("agt")
	element.send_keys("stan168")

	#取款密碼 下拉選單 第11個li依序下面的select
	pass1 = Select(driver.find_element_by_css_selector("li:nth-child(11) select:nth-child(1)"))
	pass1.select_by_value('0')

	pass1 = Select(driver.find_element_by_css_selector("li:nth-child(11) select:nth-child(2)"))
	pass1.select_by_value('0')

	pass1 = Select(driver.find_element_by_css_selector("li:nth-child(11) select:nth-child(3)"))
	pass1.select_by_value('0')

	pass1 = Select(driver.find_element_by_css_selector("li:nth-child(11) select:nth-child(4)"))
	pass1.select_by_value('0')

	element = driver.find_element_by_id("btn_add_f").click()

	#確定alert
	time.sleep(1)
	driver.switch_to.alert.accept()

while True:
	mem_add()
