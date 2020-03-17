# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re , os , time ,random ,string ,logging

#打開網頁,最大化瀏覽器
driver = webdriver.Chrome()
driver.get("https://ku112.net/")
driver.maximize_window()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
 
#logger.debug('Debugging')
#logger.warning('Warning exists')
#logger.info('Finish')

#找到輸入框->輸入內容
driver.find_element_by_id("loginbutton").click()

element = driver.find_element_by_id("accountId")
element.send_keys("F62127")

element = driver.find_element_by_name("accountPwd")
element.send_keys("qaz123")

logger.info('Before Login Time') #紀錄登錄前的時間
driver.find_element_by_id("signin").click()

def tryclick(count=0): ##保護機制，以防無法定位到還沒渲染出來的元素
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

def tryclick1(count=0): ##保護機制，以防無法定位到還沒渲染出來的元素
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

def tryclick2(count=0): ##保護機制，以防無法定位到還沒渲染出來的元素
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
tryclick1()
tryclick2()
logger.info('Close PlatfromTransfer Time / OpenLiveService Time') #紀錄選擇轉出帳戶/轉入帳戶完的時間
driver.close()

#找到原視窗,並切換過去
for parentHandle in driver.window_handles:
	driver.switch_to.window(parentHandle)

driver.find_element_by_xpath("/html/body/div[9]/div[1]/ul/li[1]/div").click() #點擊在線客服

#找到在線客服視窗,並切換過去
for winHandle in driver.window_handles:
	driver.switch_to.window(winHandle)

def tryclick1(count=0): ##保護機制，以防無法定位到還沒渲染出來的元素
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