# coding:utf-8
from functools import reduce
from selenium import webdriver
from PIL import Image,ImageEnhance
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import logging,time,threading,os

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

#設定log格式
logging.basicConfig(filename='CNLogin.log',
                    level=logging.INFO ,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y/%m/%d %I:%M:%S %p')
logger = logging.getLogger(__name__)

#將time格式化爲具有毫秒的字符串
def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 100
    time_stamp = "%s.%02d" % (data_head, data_secs)
    stamp = ("".join(time_stamp.split()[0].split(":"))).replace('.', '')
    return stamp

#用來更改檔名時間
def get_time_stamp1():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d", local_time)
    return data_head

#截圖保存位置
screenImg01 = "C:/Users/Stanhsu/.PyCharmCE2019.3/config/scratches/image/screenImg01.png"
screenImg02 = "C:/Users/Stanhsu/.PyCharmCE2019.3/config/scratches/image/screenImg02.png"

#多執行緒中斷
class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

#https://ku.ku665.net/
#https://ku.ku3699.net/
#https://ku.ku5168.com/
#https://ku.ku9688.net/
#https://ku.ku997.com/

net = "https://ku.ku9688.net/"

#ku測速一回
def auto():
    #打開網頁,最大化瀏覽器
    hometime = int(get_time_stamp())
    driver = webdriver.Chrome(options=options)
    driver.get("%s" %net)
    logger.info('*******************************************************')
    logger.info('%s',driver.current_url)
    hometime1 = int(get_time_stamp())
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
    logintime = int(get_time_stamp())

    #點擊登入
    driver.find_element_by_id("signin").click()

    #等待首頁平台轉帳渲染
    WebDriverWait(driver, 15).until(
    ec.element_to_be_clickable((By.CSS_SELECTOR,"body > div.toper > div > div.ng-scope > div.memberArea.ng-scope > ul > li:nth-child(5) > a")))

    #等待首頁存款渲染
    WebDriverWait(driver, 15).until(
    ec.element_to_be_clickable((By.CSS_SELECTOR,"body > div.toper > div > div.ng-scope > div.memberArea.ng-scope > ul > li:nth-child(6) > a")))

    #等待首頁提款渲染
    WebDriverWait(driver, 15).until(
    ec.element_to_be_clickable((By.CSS_SELECTOR,"body > div.toper > div > div.ng-scope > div.memberArea.ng-scope > ul > li:nth-child(7) > a")))

    #紀錄點擊平台轉帳時間
    logger.info('After Login Time / Open PlatfromTransfer Time')
    logintime1 = int(get_time_stamp())

    #此function為點擊平台轉帳
    def tryclick(driver0, selector, count=0): #保護機制,以防無法定位到還沒渲染出來的元素
        # noinspection PyBroadException
        try:
            driver0.find_element_by_css_selector(selector).click()
        except:
            time.sleep(0.5)
            count+=0.5
            if count < 2:
                tryclick(driver0, selector, count)
            else:
                print("cannot locate PlatfromTransfer")

    #首頁點擊平台轉帳
    tryclick(driver, "body > div.toper > div > div.ng-scope > div.memberArea.ng-scope > ul > li:nth-child(5) > a")

    #找到平台轉帳視窗,並切換過去
    for winHandle in driver.window_handles:
        driver.switch_to.window(winHandle)

    #此function為平台轉帳轉出帳戶欄位
    def tryclick1(driver1, selector, count=0): #保護機制,以防無法定位到還沒渲染出來的元素
        # noinspection PyBroadException
        try:
            driver1.find_element_by_css_selector(selector).click()
        except:
            time.sleep(0.5)
            count+=0.5
            if count < 2:
                tryclick1(driver1, selector, count)
            else:
                print("cannot locate transferout")

    #此function為平台轉帳轉入帳戶欄位
    def tryclick2(driver2, selector, count=0): #保護機制,以防無法定位到還沒渲染出來的元素
        # noinspection PyBroadException
        try:
            driver2.find_element_by_css_selector(selector).click()
        except:
            time.sleep(0.5)
            count+=0.5
            if count < 2:
                tryclick2(driver2, selector, count)
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
    logintime2 = int(get_time_stamp())

    #關閉平台轉帳視窗
    driver.close()

    #找到原視窗,並切換過去
    for parentHandle in driver.window_handles:
        driver.switch_to.window(parentHandle)

    #點擊在線客服
    driver.find_element_by_xpath("/html/body/div[9]/div[1]/ul/li[1]/div").click()
    servicetime = int(get_time_stamp())

    #找到原視窗,並切換過去
    for winHandle in driver.window_handles:
        driver.switch_to.window(winHandle)

    #等待在線客服視窗渲染
    WebDriverWait(driver, 10).until(
    ec.element_to_be_clickable((By.XPATH,"//*[@id='main-block']/ul[1]/li[2]/div/div[2]/a[1]/img")))

    #紀錄在線客服開啟時間
    logger.info('Catch CustomerService Time')
    servicetime1 = int(get_time_stamp())

    #顯示當前在線客服的url
    logger.info('%s',driver.current_url)

    #此function為在線客服截圖與照片處理
    def code_func():
        #照片url位址
        driver.find_element_by_xpath("//*[@id='main-block']/ul[1]").get_attribute('src')

        #截畫面
        driver.get_screenshot_as_file(screenImg01)

        #定位圖片位置及大小
        location = driver.find_element_by_xpath("//*[@id='main-block']/ul[1]").location
        size = driver.find_element_by_xpath("//*[@id='main-block']/ul[1]").size
        left = location['x']
        top =  location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        #從讀取照片，截取圖片位置再次保存
        time.sleep(0.5)
        img = Image.open(screenImg01).crop((left,top,right,bottom))
        img = img.convert('L')           #轉換模式：L | RGB
        img = ImageEnhance.Contrast(img) #增強對比度
        img = img.enhance(2)             #增加飽和度
        img.save(screenImg01)

    #此function為3D電子截圖與照片處理
    def code_func1():
        #照片url位址
        driver.find_element_by_xpath("//*[@id='launcherMain']").get_attribute('src')

        #截畫面
        driver.get_screenshot_as_file(screenImg02)

        #定位圖片位置及大小
        location = driver.find_element_by_xpath("//*[@id='launcherMain']").location
        size = driver.find_element_by_xpath("//*[@id='launcherMain']").size
        left = location['x']
        top =  location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        #從讀取照片,截取圖片位置再次保存
        time.sleep(0.5)
        img = Image.open(screenImg02).crop((left,top,right,bottom))
        img = img.convert('L')           #轉換模式：L | RGB
        img = ImageEnhance.Contrast(img) #增強對比度
        img = img.enhance(2)             #增加飽和度
        img.save(screenImg02)

    #計算圖片的局部哈希值--pHash
    def phash(img):
        #param img: 圖片
        #return: 返回圖片的局部hash值

        img = img.resize((8, 8), Image.ANTIALIAS).convert('L')
        avg = reduce(lambda x, y: x + y, img.getdata()) / 64.
        hash_value=reduce(lambda x, y: x | (y[1] << y[0]), enumerate(map(lambda ii: 0 if ii < avg else 1, img.getdata())), 0)
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

        return True if hamming_distance(phash(img1),phash(img2)) <= 1 else False

    #在線客服截圖
    code_func()

    #比對在線客服圖片
    if __name__ == '__main__':
        #讀取圖片
        sensitive_pic = Image.open("C:/Users/Stanhsu/.PyCharmCE2019.3/config/scratches/CorrectCustomerService.png")
        target_pic = Image.open("C:/Users/Stanhsu/.PyCharmCE2019.3/config/scratches/image/screenImg01.png")

        #比較圖片相似度
        result=is_imgs_similar(target_pic, sensitive_pic)
        logger.info('CustomerService Compare Result : %s',result)

    #關閉在線客服視窗
    driver.close()

    #找到原視窗,並切換過去
    for parentHandle in driver.window_handles:
        driver.switch_to.window(parentHandle)

    # 找到電子遊戲->點擊3D電子
    element_to_hover_over = driver.find_element_by_xpath("//*[@id='MainMenu']/div/div[1]/div[2]/ul/li[7]/a")
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()
    driver.find_element_by_xpath("//*[@id='MainMenu']/div/div[1]/div[2]/ul/li[7]/div/div[2]/div[4]/div[2]/div[2]").click()

    #等待快速轉帳視窗渲染
    WebDriverWait(driver, 10).until(
    ec.element_to_be_clickable((By.CSS_SELECTOR,"#FastTransfer > form > div.popUp_in > div > div > input.FT_button_w50L")))

    # 印出3D電子金額
    element1 = driver.find_elements_by_xpath('//*[@id="FastTransfer"]/form/div[2]/div/ul/li[2]/div/div[1]')[0].text
    print(element1)

    #此function為抓取快速轉帳
    def tryclick3(driver3, xpath, count=0):#保護機制,以防無法定位到還沒渲染出來的元素
        # noinspection PyBroadException
        try:
            driver3.find_element_by_xpath(xpath).click()
        except:
            time.sleep(0.5)
            count+=0.5
            if count < 2:
                tryclick3(driver3, xpath, count)
            else:
                print("cannot locate FastTransfer")

    tryclick3(driver, "//*[@id='FastTransfer']/form/div[2]/div")

    #此function為進入3D電子遊戲
    def tryclick4(driver4, selector, count=0): #保護機制,以防無法定位到還沒渲染出來的元素
        # noinspection PyBroadException
        try:
            driver4.find_element_by_css_selector(selector).click()
        except:
            time.sleep(0.5)
            count+=0.5
            if count < 2:
                tryclick4(driver4, selector, count)
            else:
                print("cannot locate Enter3Dgame")

    tryclick4(driver, "#FastTransfer > form > div.popUp_in > div > div > input.FT_button_w50L")

    #紀錄開啟3D電子的時間
    logger.info('Open 3Dgame Time')
    threedtime = int(get_time_stamp())

    #找到3D電子視窗,並切換過去
    for winHandle in driver.window_handles:
        driver.switch_to.window(winHandle)

    #多執行緒五個banner
    def tryclick5(driver5, xpath , count=0): #保護機制,以防無法定位到還沒渲染出來的元素
        # noinspection PyBroadException
        try:
            driver5.find_element_by_xpath(xpath).click()
        except:
            time.sleep(0.5)
            count+=0.5
            if count < 3:
                tryclick5(driver5, xpath, count)
            else:
                print("cannot locate 3DgameCarousel")

    def thread_job1():
        tryclick5(driver, "//*[@id='canvas_0002']")

    def thread_job2():
        tryclick5(driver, "//*[@id='canvas_1054']")

    def thread_job3():
        tryclick5(driver, "//*[@id='canvas_1045']")

    def thread_job4():
        tryclick5(driver, "//*[@id='canvas_1038']")

    def thread_job5():
        tryclick5(driver, "//*[@id='canvas_0001']")

    def main():
        thread1 = threading.Thread(target=thread_job1)
        thread2 = threading.Thread(target=thread_job2)
        thread3 = threading.Thread(target=thread_job3)
        thread4 = threading.Thread(target=thread_job4)
        thread5 = threading.Thread(target=thread_job5)

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()

        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        print('all done')

    c = CountdownTask()
    t = threading.Thread(target=main)
    t.start()
    c.terminate()
    t.join()

    #紀錄輪播圖渲染完時間
    threedtime1 = int(get_time_stamp())
    logger.info('Show Carousel Time')

    #顯示當前3D電子url
    logger.info('%s',driver.current_url)

    #3D電子截圖
    code_func1()

    #比對3D電子圖片
    if __name__ == '__main__':
        #讀取圖片
        sensitive_pic = Image.open("C:/Users/Stanhsu/.PyCharmCE2019.3/config/scratches/Correct3Dgmae.png")
        target_pic = Image.open("C:/Users/Stanhsu/.PyCharmCE2019.3/config/scratches/image/screenImg02.png")

        #比較圖片相似度
        result=is_imgs_similar(target_pic, sensitive_pic)
        logger.info('3Dgame Compare Result : %s',result)

    #關閉3D電子視窗
    driver.close()

    #找到原視窗,並切換過去
    for parentHandle in driver.window_handles:
        driver.switch_to.window(parentHandle)

    #找到彩票遊戲->點擊全球
    element_to_hover_over = driver.find_element_by_xpath("//*[@id='MainMenu']/div/div[1]/div[2]/ul/li[9]/a")
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()
    driver.find_element_by_xpath("//*[@id='BB_Ball_loto_maintain']/div[3]/div").click()

    #等待快速轉帳視窗渲染
    WebDriverWait(driver, 10).until(
    ec.element_to_be_clickable((By.CSS_SELECTOR,"#FastTransfer > form > div.popUp_in > div > div > input.FT_button_w50L")))

    #為抓取快速轉帳
    tryclick3(driver, "//*[@id='FastTransfer']/form/div[2]/div")
    #為進入全球彩票
    tryclick4(driver, "#FastTransfer > form > div.popUp_in > div > div > input.FT_button_w50L")

    #找到全球彩票視窗,並切換過去
    for winHandle in driver.window_handles:
        driver.switch_to.window(winHandle)

    #等待全球彩票金額渲染
    element1 = WebDriverWait(driver, 10).until(
    ec.text_to_be_present_in_element((By.ID,"divBalance"),"12"))
    logger.info('Lottery Money Catch Result : %s',element1)

    #關閉全球彩票視窗
    driver.close()

    #找到原視窗,並切換過去
    for parentHandle in driver.window_handles:
        driver.switch_to.window(parentHandle)

    #關閉視窗
    driver.close()

    print('-----------------------------')
    print('第{}次首頁時間 : {}'.format(times , hometime1 - hometime))
    print('第{}次登入時間 : {}'.format(times , logintime1-logintime))
    print('第{}次平台轉帳 : {}'.format(times , logintime2-logintime1))
    print('第{}次在線客服 : {}'.format(times , servicetime1-servicetime))
    print('第{}次3D電子 : {}'.format(times , threedtime1-threedtime))
    print('第{}次全球彩票 : {}'.format(times , element1))
    print('-----------------------------')

auto()

# #次數從1開始
# times = 1
# while times < 6 :
#     auto()
#     path = 'C:/Users/Stanhsu/.PyCharmCE2019.3/config/scratches/image/'  #欲進行檔名更改的檔案路徑
#     files = os.listdir(path)
#
#     number =  0
#     for i in files:
#         oldname = path + files[number]  # 指出檔案現在的路徑名稱，[n]表示第n個檔案
#         newname = path + get_time_stamp1() + '-' + str(number+1) + '.png'
#         os.rename(oldname, newname)
#         number = number + 1
#     times = times + 1
# input()