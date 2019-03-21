# coding:utf-8
from selenium import webdriver
from PIL import Image , ImageEnhance
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract , re , requests , os , time ,random ,string

#抓取驗驗證碼code_func
def code_func():
	#先點擊驗整碼欄位
	element = driver.find_element_by_id("captcha_code").click()

	#驗證碼url位址
	imgsrc = driver.find_element_by_id("captcha_code").get_attribute('src')

	#截畫面
	driver.get_screenshot_as_file(screenImg)

	#定位驗證碼位置及大小
	location = driver.find_element_by_css_selector("[class='pointer']").location
	size = driver.find_element_by_css_selector("[class='pointer']").size
	left = location['x']
	top =  location['y']
	right = location['x'] + size['width']
	bottom = location['y'] + size['height']

	#從文件讀取截圖，截取驗證碼位置再次保存
	time.sleep(1)
	img = Image.open(screenImg).crop((left,top,right,bottom))
	img = img.convert('L') 			 #轉換模式：L | RGB
	img = ImageEnhance.Contrast(img) #增強對比度
	img = img.enhance(2)			 #增加飽和度
	img.save(screenImg)

	#再次讀取與識別驗證碼
	img = Image.open(screenImg)
	code = pytesseract.image_to_string(img,lang='eng',config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

	#登入
	driver.find_element_by_id("captcha_code").send_keys(code)
	driver.find_element_by_css_selector("[class='btn btn-warning']").click()

#截圖或驗證碼圖片保存位置
screenImg = "C:/Users/20180312/screenImg.png"

#打開網頁,最大化瀏覽器
driver = webdriver.Chrome()
driver.get("http://www.zzxx88.com/")
driver.maximize_window()

#找到輸入框->輸入內容
element = driver.find_element_by_id("ipt_acc")
element.send_keys("20180312")

element = driver.find_element_by_id("ipt_pwd")
element.send_keys("z1x2c3v4b5")
code_func()

#判斷alert彈出框,假如有彈出窗則再進行一次輸入驗證碼
alert = True
while alert:
    try:
        time.sleep(1)
        driver.switch_to.alert.accept()
        time.sleep(1)
        driver.find_element_by_id("captcha_code").clear()
        code_func()
    except:
        alert = False

time.sleep(3)
element = driver.find_element_by_css_selector("[class='glyphicon glyphicon-bell']").click()
driver.switch_to.alert.accept()