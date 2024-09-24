'''
Created on 2023年3月13日

@author: bond9
'''

from bs4 import BeautifulSoup
import requests
import cv2

def searchByMovieName(movieName):
    try:
        url = "https://movies.yahoo.com.tw/moviesearch_result.html?keyword=" + movieName +"&type=movie&movie_type=all"
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        sel = soup.select("div.release_movie_name a")
        selChinese = []
        selEnglish = []
        for k in range(len(sel)//2):
            selChinese.append(sel[k*2])
            selEnglish.append(sel[k*2+1])
        try:
            selPage = soup.select("div.page_numbox li")
            if (len(selPage)-4 > 1):
                for i in range(2, len(selPage)-3, 1):
                    url = "https://movies.yahoo.com.tw/moviesearch_result.html?keyword=" + movieName +"&type=movie&movie_type=all&page=" + str(i)
                    r = requests.get(url)
                    soup = BeautifulSoup(r.text,"html.parser")
                    sel = soup.select("div.release_movie_name a")
                    for k in range(len(sel)//2):
                        selChinese.append(sel[k*2])
                        selEnglish.append(sel[k*2+1])
        except:
            pass
        # j = 1
        # for i in range(len(selChinese)):
        #     print(j)
        #     print(selChinese[i].text)
        #     print(selChinese[i]["href"])
        #     j +=1
        return selChinese
    except:
        return -1

def searchByUrl(url):
    try:
        informationList = ["名稱", "類型", "片長", "上映日期", "導演", "IMDb分數", "發行公司", "story"]
        informationList = ["null"]*len(informationList)
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        sel = soup.select("span")
        sel2 = soup.select("span.movie_intro_list")
        selName = soup.select("div.movie_intro_info_r h1")
        informationList[0] = selName[0].text.replace("\n", "").replace(" ", "")
        selType = soup.select("div.level_name a")
        selType2 = ""
        for i in range(len(selType)):
            if i != 0:
                selType2 += " "
            selType2 += selType[i].text.replace("\n", "").replace(" ", "")
        informationList[1] = selType2
        for i in range(len(sel)):
            if sel[i].text.find("上映日期：") != -1:
                informationList[3] = sel[i].text
            elif sel[i].text.find("片　　長：") != -1:
                informationList[2] = sel[i].text.replace("　", "")
            elif sel[i].text.find("發行公司：") != -1:
                informationList[6] = sel[i].text
            elif sel[i].text.find("IMDb分數：") != -1:
                informationList[5] = sel[i].text
        for j in range(len(sel2)):
            if sel2[j].text.find("導演：") != -1:
                informationList[4] = "".join(sel2[j].text.replace("\n", "").split())
        selPhoto = soup.select("div.movie_intro_foto img")
        img = requests.get(selPhoto[0]["src"]).content
        pic_out = open('src/static/img.jpg','wb')
        pic_out.write(img)
        pic_out.close()
        selStory = soup.select("span#story")
        informationList[7] = selStory[0].text.replace(" ", "").replace("\n\n", "\n").strip("\n")
        return informationList
    except:
        return -1

def moiveTopCharts(): # 台北電影票房排行榜
    outputList = []
    r = requests.get("https://movies.yahoo.com.tw/chart.html") # 將網頁資料GET下來
    soup = BeautifulSoup(r.text,"html.parser") # 將網頁資料以html.parser
    sel = soup.select("div.td h2") # 取HTML標中的 <div class="td"></div> 中的<h2>標籤存入sel
    sel += soup.select("div.rank_txt") # 取HTML標中的 <div class="rank_txt"></div> 存入sel
    sel2 = soup.select("div.td") # 取HTML標中的 <div class="td"></div> 存入sel2
    i = 1
    j = 11
    k = 13
    for s in sel:
        subList = []
        subList.append(i)
        subList.append(s.text)
        subList.append(sel2[j].text)
        subList.append(sel2[k].text.replace("\n", ""))
        outputList.append(subList)
        # print(i, end=" ")
        # print(s.text, end="  ")
        # print(sel2[j].text, end="  ")
        # print(sel2[k].text.replace("\n", ""))
        i += 1
        j += 7
        k += 7
    return outputList



def test():

    print("請輸入欲查詢的名稱") #範例使用
    moiveName = input()
    result = searchByMovieName(moiveName)
    if len(result) > 1:
        for i in range(len(result)):
            print(result[i].text)
        print("Please choice whice you want to search by using enter 1 ~ ", end="")
        print(len(result))
        movieNumbe = 0
        while(1):
            movieNumber = int(input())
            if movieNumber > 0 and movieNumber <= len(result):
                break
            else:
                print("請輸入範圍內的數字")
        result2 = searchByUrl(result[movieNumber - 1]["href"])
    else:
        result2 = searchByUrl(result[0]["href"])
    print(result2)
    a = moiveTopCharts() # moiveTopCharts Test
    for i in range(len(a)):
        print("排名" + str(a[i][0]) + " " + a[i][1] + " 上映日期: " + a[i][2] + " 網友滿意度: " + a[i][3])
    img = cv2.imread('src/static/img.jpg')
    cv2.imshow('My Image', img)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()

#test()
# ['蟻人與黃蜂女', '動作 科幻', '片長：01時59分', '上映日期：2018-07-04', '導演：派頓瑞德(PeytonReed)', 'IMDb分數：7.5', '發行公司：迪士尼影業', '故事接續在《美國隊長3：英雄內戰》之後，史考特朗恩因為參與了內戰判刑，帶上電子腳鐐，居家監禁，在父親和蟻人兩個角色中左支右絀。眼看刑期終於快服滿，皮姆博士和荷普又帶著危急的任務找上門，史考特不得不再次穿上蟻人裝束，與黃蜂女一起對抗來自過去的黑暗秘密。']