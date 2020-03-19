# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re , os , time ,random ,string ,logging ,pytesseract ,requests

#截圖保存位置
screenImg = "D:/Users/Stanhsu/Desktop/git-example/image/screenImg.png"

#打開網頁,最大化瀏覽器
driver = webdriver.Chrome()
driver.get("https://ku112.net/")
driver.maximize_window()

#引入logging模組,設定基本的配置
#basicConfig配置了level和format的訊息;Level配置為INFO訊息
#指定了format格式的字串,包括asctime、name、levelname、message分别代表運行時間、模組名稱、日誌級別、日誌內容。
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
 
#logger.debug('Debugging')
#logger.warning('Warning exists')
#logger.info('Finish')

#找到登入->點擊登入->輸入內容
driver.find_element_by_id("loginbutton").click()

element = driver.find_element_by_id("accountId")
element.send_keys("F62127")

element = driver.find_element_by_name("accountPwd")
element.send_keys("qaz123")

logger.info('Before Login Time') #紀錄登錄前的時間
driver.find_element_by_id("signin").click()

def tryclick(count=0): #保護機制，以防無法定位到還沒渲染出來的元素
    try:
        driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]").click() #先選框
        driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/ul/li[5]/a/span").click() #再點擊
        logger.info('After Login Time / Open PlatfromTransfer Time') #紀錄點擊平台轉帳時間
    except:
        time.sleep(0.5)
        count = count+0.5
        if(count <2):
            tryclick(count)
        else:
            print("cannot locate PlatfromTransfer")

#首頁點擊平台轉帳
tryclick()

#找到平台轉帳視窗,並切換過去
for winHandle in driver.window_handles:
	driver.switch_to.window(winHandle)

def tryclick1(count=0): #保護機制，以防無法定位到還沒渲染出來的元素
    try:
        transferout = Select(driver.find_element_by_xpath("//*[@id='tbPlatformTransfer']/tbody/tr/td[2]/div/ul/li[1]/select")) #選擇轉出帳戶輸入框
        try:
            transferout.select_by_index(1) #選擇輸入框第二項(以0開始計算)
        except:
            time.sleep(0.5)
            count = count+0.5
            if(count <2):
                tryclick(count)
            else:
                print("cannot locate index")
    except:
        time.sleep(0.5)
        count = count+0.5
        if(count <2):
            tryclick(count)
        else:
            print("cannot locate transferout")

def tryclick2(count=0): #保護機制，以防無法定位到還沒渲染出來的元素
    try:
        transferin = Select(driver.find_element_by_xpath("//*[@id='inAccount']")) #選擇轉入帳戶輸入框
        try:
            transferin.select_by_index(1) #選擇輸入框第二項(以0開始計算)
        except:
            time.sleep(0.5)
            count = count+0.5
            if(count <2):
                tryclick(count)
            else:
                print("cannot locate transferin")
    except:
        time.sleep(0.5)
        count = count+0.5
        if(count <2):
            tryclick(count)
        else:
            print("cannot locate transferout")

#平台轉帳內的轉出帳戶欄位選擇第二項(KU真人)
tryclick1()

#平台轉帳內的轉入帳戶欄位選擇第二項(KU體育)
tryclick2()

logger.info('Close PlatfromTransfer Time / OpenLiveService Time') #紀錄選擇轉出帳戶/轉入帳戶完的時間

#關閉平台轉帳視窗
driver.close()

#找到原視窗,並切換過去
for parentHandle in driver.window_handles:
	driver.switch_to.window(parentHandle)

driver.find_element_by_xpath("/html/body/div[9]/div[1]/ul/li[1]/div").click() #點擊在線客服

#找到在線客服視窗,並切換過去
for winHandle in driver.window_handles:
	driver.switch_to.window(winHandle)

def code_func():
	#照片url位址
    imgsrc = driver.find_element_by_xpath("//*[@id='main-block']/ul[1]/li[2]/div/div[2]/a[1]").get_attribute('src')

	#截畫面
    driver.get_screenshot_as_file(screenImg)

	#定位圖片位置及大小
    location = driver.find_element_by_xpath("//*[@id='main-block']/ul[1]/li[2]/div/div[2]/a[1]").location
    size = driver.find_element_by_xpath("//*[@id='main-block']/ul[1]/li[2]/div/div[2]/a[1]").size
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

def tryclick3(count=0): #保護機制，以防無法定位到還沒渲染出來的元素
    try:
        code_func() #
    except:
        time.sleep(0.5)
        count = count+0.5

#在線客服截圖
tryclick3()

#計算圖片的局部哈希值--pHash
def phash(img):

    #param img: 圖片
    #return: 返回圖片的局部hash值

    img = img.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, img.getdata()) / 64.
    hash_value=reduce(lambda x, y: x | (y[1] << y[0]), enumerate(map(lambda i: 0 if i < avg else 1, img.getdata())), 0)
    print(hash_value)
    return hash_value

#計算漢明距離:
def hamming_distance(a, b):

    #param a: 圖片1的hash值
    #param b: 圖片2的hash值
    #return: 返回兩個圖片hash值的漢明距離

    hm_distance=bin(a ^ b).count('1')
    print(hm_distance)
    return hm_distance

#計算兩個圖片是否相似:
def is_imgs_similar(img1,img2):

    #param img1: 圖片1
    #param img2: 圖片2
    #return:  True 圖片相似 ; False 圖片不相似

    return True if hamming_distance(phash(img1),phash(img2)) <= 1 else False

if __name__ == '__main__':

    #讀取圖片
    sensitive_pic = Image.open("D:/Users/Stanhsu/Desktop/git-example/image/CorrectCustomerService.png")
    target_pic = Image.open("D:/Users/Stanhsu/Desktop/git-example/image/screenImg.png")

    #比較圖片相似度
    result=is_imgs_similar(target_pic, sensitive_pic)

    print(result)
    logger.info('Compare Time') #紀錄比對完的時間

#關閉在線客服視窗
driver.close()

#找到原視窗,並切換過去
for parentHandle in driver.window_handles:
	driver.switch_to.window(parentHandle)

