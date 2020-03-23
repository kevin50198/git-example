# coding:utf-8
from functools import reduce
from selenium import webdriver
from PIL import Image , ImageEnhance
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging ,pytesseract ,requests ,time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

#截圖保存位置
screenImg = "D:/Users/Stanhsu/Desktop/git-example/image/screenImg.png"
screenImg1 = "D:/Users/Stanhsu/Desktop/git-example/image/screenImg1.png"

#logging級別NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
logger = logging.getLogger("name")
logger.setLevel(logging.INFO)

# 建立一個filehandler來把日誌記錄在檔案裡，級別為info以上
fh = logging.FileHandler("CNLogin.log")
fh.setLevel(logging.INFO)

# 建立一個streamhandler來把日誌打在CMD視窗上，級別為info以上
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# 設定日誌格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)

#將相應的handler新增在logger物件中
logger.addHandler(ch)
logger.addHandler(fh)

#開始打日誌
# logger.debug("debug message")
# logger.info("info message")
# logger.warning("warn message")
# logger.error("error message")
# logger.critical("critical message")

#打開網頁,最大化瀏覽器
driver = webdriver.Chrome(options=options)
driver.get("https://ku112.net")
driver.maximize_window()

#找到登入->點擊登入
driver.find_element_by_id("loginbutton").click()

#輸入帳號/密碼
element = driver.find_element_by_id("accountId")
element.send_keys("F62126")
element = driver.find_element_by_name("accountPwd")
element.send_keys("qaz123")

#紀錄點擊登錄前的時間
logger.info('Before Login Time')

#點擊登入
driver.find_element_by_id("signin").click()

#等待首頁平轉轉帳渲染
element = WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div.toper > div > div.ng-scope > div.memberArea.ng-scope > ul > li:nth-child(5) > a")))

#此function為點擊平台轉帳
def tryclick(driver, selector, count=0): #保護機制,以防無法定位到還沒渲染出來的元素
    try:
        element = driver.find_element_by_css_selector(selector)
        element.click()
    except:
        time.sleep(0.5)
        count+=0.5
        if(count < 2):
            tryclick(driver, selector, count)
        else:
            print("cannot locate PlatfromTransfer")

#首頁點擊平台轉帳
tryclick(driver, "body > div.toper > div > div.ng-scope > div.memberArea.ng-scope > ul > li:nth-child(5) > a")

#紀錄點擊平台轉帳時間
logger.info('After Login Time / Open PlatfromTransfer Time')

#找到平台轉帳視窗,並切換過去
for winHandle in driver.window_handles:
	driver.switch_to.window(winHandle)

#此function為平台轉帳轉出帳戶欄位
def tryclick1(driver, selector, count=0): #保護機制,以防無法定位到還沒渲染出來的元素
    try:
        element = driver.find_element_by_css_selector(selector)
        element.click()
    except:
        time.sleep(0.5)
        count+=0.5
        if(count < 2):
            tryclick1(driver, selector, count)
        else:
            print("cannot locate transferout")

#此function為平台轉帳轉入帳戶欄位
def tryclick2(driver, selector, count=0): #保護機制,以防無法定位到還沒渲染出來的元素
    try:
        element = driver.find_element_by_css_selector(selector)
        element.click()
    except:
        time.sleep(0.5)
        count+=0.5
        if(count < 2):
            tryclick2(driver, selector, count)
        else:
            print("cannot locate transferin")

#轉出帳戶->選擇第三項(KU真人)
tryclick1(driver, "#tbPlatformTransfer > tbody > tr > td:nth-child(2) > div > ul > li:nth-child(1) > select")
tryclick1(driver, "#tbPlatformTransfer > tbody > tr > td:nth-child(2) > div > ul > li:nth-child(1) > select > option:nth-child(3)")

#轉入帳戶->選擇第二項(KU體育)
tryclick2(driver, "#inAccount")
tryclick2(driver, "#inAccount > option:nth-child(2)")

#紀錄選擇轉出帳戶/轉入帳戶後的時間
logger.info('Close PlatfromTransfer Time / OpenLiveService Time')

#關閉平台轉帳視窗
driver.close()

#找到原視窗,並切換過去
for parentHandle in driver.window_handles:
	driver.switch_to.window(parentHandle)

#點擊在線客服
driver.find_element_by_xpath("/html/body/div[9]/div[1]/ul/li[1]/div").click()

#找到在線客服視窗,並切換過去
for winHandle in driver.window_handles:
	driver.switch_to.window(winHandle)

#等待在線客服視窗渲染
element = WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.XPATH,"//*[@id='main-block']/ul[1]")))

#此function為在線客服截圖與照片處理
def code_func():
	#照片url位址
    imgsrc = driver.find_element_by_xpath("//*[@id='main-block']/ul[1]").get_attribute('src')

	#截畫面
    driver.get_screenshot_as_file(screenImg)

	#定位圖片位置及大小
    location = driver.find_element_by_xpath("//*[@id='main-block']/ul[1]").location
    size = driver.find_element_by_xpath("//*[@id='main-block']/ul[1]").size
    left = location['x']
    top =  location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
	#從讀取照片，截取圖片位置再次保存
    time.sleep(0.5)
    img = Image.open(screenImg).crop((left,top,right,bottom))
    img = img.convert('L') 			 #轉換模式：L | RGB
    img = ImageEnhance.Contrast(img) #增強對比度
    img = img.enhance(2)			 #增加飽和度
    img.save(screenImg)
	#再次讀取與識別圖片
	#img = Image.open(screenImg)
	#code = pytesseract.image_to_string(img,lang='eng',config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

#此function為3D電子截圖與照片處理
def code_func1():
	#照片url位址
    imgsrc = driver.find_element_by_xpath("//*[@id='launcherMain']").get_attribute('src')

	#截畫面
    driver.get_screenshot_as_file(screenImg1)

	#定位圖片位置及大小
    location = driver.find_element_by_xpath("//*[@id='launcherMain']").location
    size = driver.find_element_by_xpath("//*[@id='launcherMain']").size
    left = location['x']
    top =  location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

	#從讀取照片,截取圖片位置再次保存
    time.sleep(0.5)
    img = Image.open(screenImg1).crop((left,top,right,bottom))
    img = img.convert('L') 			 #轉換模式：L | RGB
    img = ImageEnhance.Contrast(img) #增強對比度
    img = img.enhance(2)			 #增加飽和度
    img.save(screenImg1)
	#再次讀取與識別圖片
	#img = Image.open(screenImg)
	#code = pytesseract.image_to_string(img,lang='eng',config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

#在線客服截圖
code_func()

#計算圖片的局部哈希值--pHash
def phash(img):

    #param img: 圖片
    #return: 返回圖片的局部hash值

    img = img.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, img.getdata()) / 64.
    hash_value=reduce(lambda x, y: x | (y[1] << y[0]), enumerate(map(lambda i: 0 if i < avg else 1, img.getdata())), 0)
    # print(hash_value)
    return hash_value

#計算漢明距離:
def hamming_distance(a, b):

    #param a: 圖片1的hash值
    #param b: 圖片2的hash值
    #return: 返回兩個圖片hash值的漢明距離

    hm_distance=bin(a ^ b).count('1')
    # print(hm_distance)
    return hm_distance

#計算兩個圖片是否相似:
def is_imgs_similar(img1,img2):

    #param img1: 圖片1
    #param img2: 圖片2
    #return:  True 圖片相似 ; False 圖片不相似

    return True if hamming_distance(phash(img1),phash(img2)) <= 3 else False

#比對在線客服圖片
if __name__ == '__main__':

    #讀取圖片
    sensitive_pic = Image.open("D:/Users/Stanhsu/Desktop/git-example/image/CorrectCustomerService.png")
    target_pic = Image.open("D:/Users/Stanhsu/Desktop/git-example/image/screenImg.png")

    #比較圖片相似度
    result=is_imgs_similar(target_pic, sensitive_pic)

    print(result)

    #紀錄照片比對完的時間
    logger.info('Compare Time')

#關閉在線客服視窗
driver.close()

#找到原視窗,並切換過去
for parentHandle in driver.window_handles:
	driver.switch_to.window(parentHandle)

#找到電子遊戲->點擊3D電子
driver.find_element_by_xpath("//*[@id='MainMenu']/div/div[1]/div[2]/ul/li[7]/a").click()
driver.find_element_by_xpath("//*[@id='MainMenu']/div/div[1]/div[2]/ul/li[7]/div/div[2]/div[4]/div[2]/div[2]").click()

#等待快速轉帳視窗渲染
element = WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.CSS_SELECTOR,"#FastTransfer > form > div.popUp_in > div > div > input.FT_button_w50L")))

#此function為抓取快速轉帳
def tryclick3(driver, Xpath, count=0):#保護機制,以防無法定位到還沒渲染出來的元素
    try:
        element = driver.find_element_by_xpath(Xpath)
        element.click()
    except:
        time.sleep(0.5)
        count+=0.5
        if(count < 2):
            tryclick3(driver, Xpath, count)
        else:
            print("cannot locate FastTransfer")

tryclick3(driver, "//*[@id='FastTransfer']/form/div[2]/div")

#此function為進入3D電子遊戲
def tryclick4(driver, selector, count=0): #保護機制,以防無法定位到還沒渲染出來的元素
    try:
        element = driver.find_element_by_css_selector(selector)
        element.click()
    except:
        time.sleep(0.5)
        count+=0.5
        if(count < 2):
            tryclick4(driver, selector, count)
        else:
            print("cannot locate Enter3Dgame")

tryclick4(driver, "#FastTransfer > form > div.popUp_in > div > div > input.FT_button_w50L")

#紀錄開啟3D電子的時間
logger.info('Open 3Dgame Time')

#找到3D電子視窗,並切換過去
for winHandle in driver.window_handles:
	driver.switch_to.window(winHandle)

#此function為定位3D電子輪播圖
def tryclick5(driver, Xpath, count=0): #保護機制,以防無法定位到還沒渲染出來的元素
    try:
        element = driver.find_element_by_xpath(Xpath)
        element.click()
    except:
        time.sleep(0.5)
        count+=0.5
        if(count < 15):
            tryclick5(driver, Xpath, count)
        else:
            print("cannot locate Enter3Dgame")

tryclick5(driver, "//*[@id='canvas_0002']")

#3D電子截圖
code_func1()

#比對3D電子圖片
if __name__ == '__main__':

    #讀取圖片
    sensitive_pic = Image.open("D:/Users/Stanhsu/Desktop/git-example/image/Correct3Dgmae.png")
    target_pic = Image.open("D:/Users/Stanhsu/Desktop/git-example/image/screenImg1.png")

    #比較圖片相似度
    result=is_imgs_similar(target_pic, sensitive_pic)
    print(result)

#紀錄輪播圖顯示的時間
logger.info('Show Carousel Time')

#關閉3D電子視窗
driver.close()

#找到原視窗,並切換過去
for parentHandle in driver.window_handles:
	driver.switch_to.window(parentHandle)

#找到彩票遊戲->點擊全球
driver.find_element_by_xpath("//*[@id='MainMenu']/div/div[1]/div[2]/ul/li[9]/a").click()
driver.find_element_by_xpath("//*[@id='BB_Ball_loto_maintain']/div[3]/div").click()

#等待快速轉帳視窗渲染
element = WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.CSS_SELECTOR,"#FastTransfer > form > div.popUp_in > div > div > input.FT_button_w50L")))

#為抓取快速轉帳
tryclick3(driver, "//*[@id='FastTransfer']/form/div[2]/div")

#為進入全球彩票
tryclick4(driver, "#FastTransfer > form > div.popUp_in > div > div > input.FT_button_w50L")

#找到全球彩票視窗,並切換過去
for winHandle in driver.window_handles:
	driver.switch_to.window(winHandle)

#等待全球彩票金額渲染
element1 = WebDriverWait(driver, 10).until(
EC.text_to_be_present_in_element((By.ID,"divBalance"),"12"))
print("result: ", element1)

#關閉全球彩票視窗
driver.close()

#找到原視窗,並切換過去
for parentHandle in driver.window_handles:
	driver.switch_to.window(parentHandle)

#關閉視窗
driver.close()