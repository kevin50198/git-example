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
	time.sleep(1)

#截圖或驗證碼圖片保存位置
screenImg = "C:/Users/20180312/Project/screenImg.png"

#打開網頁,最大化瀏覽器
driver = webdriver.Chrome()
driver.get("http://memlottery.org/")
driver.maximize_window()

#找到輸入框->輸入內容
element = driver.find_element_by_id("ipt_acc")
element.send_keys("qatest47")

element = driver.find_element_by_id("ipt_pwd")
element.send_keys("qwe123")
code_func()

#假如有抓到彈窗class就繼續做登入動作
alert = True
while alert:
	try:
		WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "modal-body")))
		time.sleep(1)
		driver.find_element_by_css_selector("[class='btn btn-primary']").click()
		time.sleep(1)
		driver.find_element_by_id("ipt_valid").clear()
		code_func()
	except:
		alert = False

#首頁點擊購彩大廳
driver.find_element_by_css_selector("[class='ToLobby']").click()

#找到新視窗,並切換過去
for winHandle in driver.window_handles:
	driver.switch_to.window(winHandle)

# 切回原本的視窗
# driver.switchTo().window(parentHandle);

#點擊北京賽車 ->富博PK10
time.sleep(1)
driver.find_element_by_css_selector("[class='gamelogo-game-type-3']").click()
time.sleep(1)
driver.find_element_by_xpath("//*[@id='GameList']/div[4]/div[2]/a[2]").click()

# -------------------------------------------------------------------------------------------
# 點擊前一 ->前一直選-複式(10注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[1]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div/label[1]/i").click()
# 複式全選 ->添加注單
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()

# 點擊前二 ->前二直選-複式(90注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[2]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div/label[1]/i").click()
# 複式全選 ->添加注單
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()

# 點擊前二 ->前二直選-單式(90注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[2]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div/label[2]/i").click()
# 單式讀檔傳值 ->添加注單
element = driver.find_element_by_id("BetTextarea")
f = open("C:/Users/20180312/下注/PK10前二複式.txt","r")
lines = f.readlines()
element.send_keys(lines)
driver.find_element_by_xpath("//*[@id='AddToReady']").click()

# 點擊前三 ->前三直選-複式(720注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[3]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div/label[1]/i").click()
# 複式全選 ->添加注單
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[3]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()

# 點擊前三 ->前三直選-單式(720注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[3]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div/label[2]/i").click()
# 單式讀檔傳值 ->添加注單
element = driver.find_element_by_id("BetTextarea")
f = open("C:/Users/20180312/下注/PK10前三複式.txt","r")
lines = f.readlines()
element.send_keys(lines)
driver.find_element_by_xpath("//*[@id='AddToReady']").click()

# 點擊定位膽 ->定位膽-定位膽(100注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[4]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div/label[1]/i").click()
# 定位膽全選 ->添加注單
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[3]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[4]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[5]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[6]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[7]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[8]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[9]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[10]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()

# 點擊特殊 ->特殊-大小單雙(40注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[5]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div[1]/label[1]/i").click()
# 大小單雙全選 ->添加注單
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[2]/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[2]/div[4]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[2]/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[2]/div[4]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[3]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[3]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[3]/div[2]/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[3]/div[2]/div[4]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[4]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[4]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[4]/div[2]/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[4]/div[2]/div[4]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[5]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[5]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[5]/div[2]/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[5]/div[2]/div[4]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[6]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[6]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[6]/div[2]/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[6]/div[2]/div[4]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[7]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[7]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[7]/div[2]/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[7]/div[2]/div[4]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[8]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[8]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[8]/div[2]/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[8]/div[2]/div[4]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[9]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[9]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[9]/div[2]/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[9]/div[2]/div[4]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[10]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[10]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[10]/div[2]/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[10]/div[2]/div[4]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()

# 點擊特殊 ->特殊-龍虎(10注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[5]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div[1]/label[2]/i").click()
# 龍虎全選 ->添加注單
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[3]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[3]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[4]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[4]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[5]/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[5]/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()

# 點擊特殊 ->特殊-莊閒(2注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[5]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div[1]/label[3]/i").click()
# 莊閒全選 ->添加注單
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div/div[2]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div/div[2]/div[2]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()

# 點擊特殊 ->冠亞軍-冠亞和值(17注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[5]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div[2]/label[1]/i").click()
# 冠亞和值全選 ->添加注單
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[1]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[1]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[1]/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[1]/div[4]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[1]/div[5]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[1]/div[6]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[1]/div[7]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[1]/div[8]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[1]/div[9]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[1]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[1]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[1]/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[1]/div[4]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[1]/div[5]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[1]/div[6]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[1]/div[7]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[1]/div[8]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()

# 點擊特殊 ->冠亞軍-大小單雙(4注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[5]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div[2]/label[2]/i").click()
# 大小單雙全選 ->添加注單
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div/div[3]/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div/div[3]/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div/div[3]/div[4]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()

#確認下注 -> 確認
driver.find_element_by_id("ReadyBetSend").click()
time.sleep(1)
driver.find_element_by_xpath("//*[@id='ZgCreateConfirm']/div/div/div[3]/button[1]").click()
time.sleep(3)
driver.find_element_by_xpath("//*[@id='ZgCreateAlert']/div/div/div[3]/button").click()