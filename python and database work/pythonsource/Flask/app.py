from flask import Flask,render_template  #如果要使用render_template返回渲染的模板，请在项目的主目录中加入一个目录templates
import pymysql


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    # return render_template("index.html")
    return index()

@app.route('/table')
def table():
    datalist  = []
    con = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='wxc20021212',
        db='crawldatadb',
        charset='utf8'
    )
    cur = con.cursor()
    sql = "select * from data"
    datas = cur.execute(sql)
    result=cur.fetchall()
    for item in result:
        datalist.append(item)
    cur.close()
    cur.close()
    print(datalist)
    return render_template("table.html", datas=datalist)

@app.route('/emotionhis')
def emotionhis():
    return render_template("emotionhis.html")

@app.route('/emotionpie')
def emotionpie():
    return render_template("emotionpie.html")

@app.route('/LDA')
def LDA():
    return render_template("LDA.html")

@app.route('/wordcloud')
def wordcloud():
    return render_template("wordcloud.html")

if __name__ == '__main__':
    app.run()
