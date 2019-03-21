import requests
import json
from bs4 import BeautifulSoup

r = requests.get("https://www.ptt.cc/bbs/Beauty/index.html") #將網頁資料GET下來
soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
u = soup.select("div.btn-group.btn-group-paging a")#上一頁按鈕的a標籤
url = "https://www.ptt.cc"+ u[1]["href"] #組合出上一頁的網址

for i in range(3): #往上爬3頁
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    sel = soup.select("div.title a") #標題
    u = soup.select("div.btn-group.btn-group-paging a") #a標籤
    print ("本頁的URL為"+url)
    url = "https://www.ptt.cc"+ u[1]["href"] #上一頁的網址

for s in sel: #印出網址跟標題
    print(s["href"],s.text)

#藉由首頁取得所有文章的URL
import requests
from bs4 import BeautifulSoup
import json

test = open("C:/Users/20180312/Project/test.txt","w",encoding='UTF-8')


p = requests.Session()
url=requests.get("https://www.ptt.cc/bbs/Beauty/index.html")
soup = BeautifulSoup(url.text,"html.parser")
sel = soup.select("div.title a")
# a=[]
# for s in sel:
#     a.append(s["href"])
# url = "https://www.ptt.cc/bbs"+ a[2]

# for k in range(0,10):
#         post_data={
#             "before":a[-1][9:18],
#             "limit":"30",
#             "popular":"true"
#         }
#         r = p.get("https://www.dcard.tw/_api/forums/pet/posts",params=post_data, headers = { "Referer": "https://www.dcard.tw/", "User-Agent": "Mozilla/5.0" })
#         data2 = json.loads(r.text)
#         for u in range(len(data2)):
#             Temporary_url = "/f/pet/p/"+ str(data2[u]["id"]) + "-" + str(data2[u]["title"].replace(" ","-"))
#             a.append(Temporary_url)
# j=0 #為了印頁數
# q=0 #為了印張數
# for i in a[2:]:
#     url = "https://www.dcard.tw"+i
#     j+=1
#     print ("第",j,"頁的URL為:"+url)
#     #file.write("temperature is {} wet is {}%\n".format(temperature, humidity))
#     test.write("第 {} 頁的URL為: {} \n".format(j,url))
#     url=requests.get(url)
#     soup = BeautifulSoup(url.text,"html.parser")
    
    # sel_jpg = soup.select("div.Post_content_NKEl9 div div div img.GalleryImage_image_3lGzO")
    for c in sel_jpg:
        q+=1
        print("第",q,"張:",c["src"])
        test.write("%\n""第 {} 張: {} \n".format(q,c["src"])) 
        pic=requests.get(c["src"])
        img2 = pic.content
        pic_out = open("spider/pet/"+str(q)+".png",'wb')
        pic_out.write(img2)
        pic_out.close()

test.close()
print("爬蟲結束")