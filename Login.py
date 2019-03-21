# coding:utf-8
from selenium import webdriver
from PIL import Image , ImageEnhance
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract , re , requests , os , time ,random ,string

def code_func():
	#先點擊驗整碼欄位
	element = driver.find_element_by_id("ipt_valid").click()

	#驗證碼url位址
	imgsrc = driver.find_element_by_id("ipt_valid").get_attribute('src')

	#截畫面
	driver.get_screenshot_as_file(screenImg)

	#定位驗證碼位置及大小
	location = driver.find_element_by_css_selector("[class='test-number vcodeImgLogin']").location
	size = driver.find_element_by_css_selector("[class='test-number vcodeImgLogin']").size
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
	driver.find_element_by_id("ipt_valid").send_keys(code)
	driver.find_element_by_id("Tologin").click()	

#截圖或驗證碼圖片保存位置
screenImg = "C:/Users/20180312/Project/screenImg.png"

#打開網頁,最大化瀏覽器
driver = webdriver.Chrome()
driver.get("http://www.glassshoes.info/")
driver.maximize_window()

#找到輸入框->輸入內容
element = driver.find_element_by_id("ipt_acc")
element.send_keys("stan168")

element = driver.find_element_by_id("ipt_pwd")
element.send_keys("qwe123")
code_func()

#假如有抓到彈窗class就繼續做登入動作
alert = True
while alert:
    try:
        element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "modal-body")))
        time.sleep(1)
        driver.find_element_by_css_selector("[class='btn btn-primary']").click()
        time.sleep(1)
        driver.find_element_by_id("ipt_valid").clear()
        code_func()
    except:
        alert = False