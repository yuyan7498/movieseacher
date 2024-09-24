from flask import Flask, render_template, request, jsonify
from movieCrawler import moiveTopCharts, searchByMovieName, searchByUrl

app = Flask(__name__)
topMovieChart = moiveTopCharts()

@app.route("/", methods=["GET", "POST"])
def mainPage():
    
    if request.method == "GET":
        return render_template("index.html", topMovieChart = topMovieChart)
    
    elif request.method == "POST":
        dataFromFontEnd = request.get_json()

        if dataFromFontEnd["action"] == "searchMovie":

            print("收到關鍵字：", dataFromFontEnd["movieName"])
            global searchResult
            searchResult = searchByMovieName(dataFromFontEnd["movieName"])
            resultList = []
            for result in searchResult:
                resultList.append(result.text)
            print("回傳搜尋結果：", resultList)
            



            return jsonify({
                "resultNum" : len(resultList),
                "resultList" : resultList,
            })

        elif dataFromFontEnd["action"] == "moreInfo":
            movieID = dataFromFontEnd['movieID']
            movieInfo = searchByUrl(searchResult[int(movieID.replace("resultBox", "")) - 1]["href"])

            print("回傳更多電影資訊")
            return jsonify({
                "movieInfo": movieInfo
            })



#['蟻人與黃蜂女', '動作 科幻', '片長：01時59分', '上映日期：2018-07-04', '導演：派頓瑞德(PeytonReed)', 'IMDb分數：7.5', '發行公司：迪士尼影業', '故事接續在《美國隊長3：英雄內戰》之後，史考特朗恩因為參與了內戰判刑，帶上電子腳鐐，居家監禁，在父親和蟻人兩個角色中左支右絀。眼看刑期終於快服滿，皮姆博士和荷普又帶著危急的任務找上門，史考特不得不再次穿上蟻人裝束，與黃蜂女一起對抗來自過去的黑暗秘密。']



app.run()