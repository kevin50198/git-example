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

#首頁點擊購彩大廳
driver.find_element_by_css_selector("[class='ToLobby']").click()

#找到新視窗,並切換過去
for winHandle in driver.window_handles:
    driver.switch_to.window(winHandle)

# 切回原本的視窗
# driver.switchTo().window(parentHandle);

#點擊時時彩 -> 518分分彩
driver.find_element_by_css_selector("[class='gamelogo-game-type-1']").click()
time.sleep(1)
driver.find_element_by_xpath("//*[@id='GameList']/div[2]/div[2]/a[6]").click()

# -------------------------------------------------------------------------------------------
# 點擊五星 -> 五星直選-複式(10萬注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[1]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div/label[1]/i").click()
# 萬千百拾個全選 ->添加注單 ->確認下注 ->確認
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[3]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[4]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[5]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()
driver.find_element_by_xpath("//*[@id='ReadyBetSend']").click()
driver.find_element_by_xpath("//*[@id='ZgCreateConfirm']/div/div/div[3]/button[1]").click()
time.sleep(1)
driver.find_element_by_xpath("//*[@id='ZgCreateAlert']/div/div/div[3]/button").click()
# -------------------------------------------------------------------------------------------

# --------------------------------------------------------
# 讀欓
# f = open("C:/Users/20180312/下注/五星.txt","r")
# lines = f.readlines()
# driver.find_element_by_id("BetTextarea").getText(lines)
# --------------------------------------------------------

# -----------------------------------------------------------------------------------------
# 點擊四星 -> 後四直選-複式(1萬注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[2]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div/label[1]/i").click()
# 千百拾個全選 ->添加注單 ->確認下注 ->確認
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[3]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[4]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()
driver.find_element_by_xpath("//*[@id='ReadyBetSend']").click()
driver.find_element_by_xpath("//*[@id='ZgCreateConfirm']/div/div/div[3]/button[1]").click()
time.sleep(1)
driver.find_element_by_xpath("//*[@id='ZgCreateAlert']/div/div/div[3]/button").click()
# -----------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------
# 點擊後三 -> 後三直選-複式(1千注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[3]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div[1]/label[1]/i").click()
# 百拾個全選 ->添加注單 ->確認下注 ->確認
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[3]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()
driver.find_element_by_xpath("//*[@id='ReadyBetSend']").click()
driver.find_element_by_xpath("//*[@id='ZgCreateConfirm']/div/div/div[3]/button[1]").click()
time.sleep(1)
driver.find_element_by_xpath("//*[@id='ZgCreateAlert']/div/div/div[3]/button").click()
# -----------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------
# 點擊後三 -> 後三直選-合值(1千注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[3]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div[1]/label[3]/i").click()
# 0-27全選->添加注單 ->確認下注 ->確認
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[4]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[5]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[6]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[7]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[8]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[9]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[5]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[6]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[7]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[8]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[10]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[11]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[12]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[13]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[14]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[15]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div/div[16]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div/div[2]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div/div[3]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div/div[4]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div/div[5]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div/div[6]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div/div[7]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div/div[8]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div/div[9]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div/div[10]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div/div[11]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div/div[12]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()
driver.find_element_by_xpath("//*[@id='ReadyBetSend']").click()
driver.find_element_by_xpath("//*[@id='ZgCreateConfirm']/div/div/div[3]/button[1]").click()
time.sleep(1)
driver.find_element_by_xpath("//*[@id='ZgCreateAlert']/div/div/div[3]/button").click()
# -----------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------
# 點擊後三 -> 後三直選-跨度(1千注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[3]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div[1]/label[4]/i").click()
# 跨度全選->添加注單 ->確認下注 ->確認
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div/div[3]/div[1]]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()
driver.find_element_by_xpath("//*[@id='ReadyBetSend']").click()
driver.find_element_by_xpath("//*[@id='ZgCreateConfirm']/div/div/div[3]/button[1]").click()
time.sleep(1)
driver.find_element_by_xpath("//*[@id='ZgCreateAlert']/div/div/div[3]/button").click()
# -----------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------
# 點擊後三 -> 後三直選-組合(3千注)
time.sleep(1)
driver.find_element_by_xpath("//*[@id='PlayLv1']/li[3]").click()
driver.find_element_by_xpath("//*[@id='PlayList']/div[1]/label[5]/i").click()
# 百拾個全選->添加注單 ->確認下注 ->確認
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[1]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[2]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='PlayContent']/div[2]/div[3]/div[3]/div[1]").click()
driver.find_element_by_xpath("//*[@id='AddToReady']").click()
driver.find_element_by_xpath("//*[@id='ReadyBetSend']").click()
driver.find_element_by_xpath("//*[@id='ZgCreateConfirm']/div/div/div[3]/button[1]").click()
time.sleep(1)
driver.find_element_by_xpath("//*[@id='ZgCreateAlert']/div/div/div[3]/button").click()
# -----------------------------------------------------------------------------------------
