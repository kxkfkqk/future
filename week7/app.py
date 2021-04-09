from flask import Flask
from flask import request
from flask import redirect
import json
from flask import render_template
from flask import session
import pymysql
import urllib.request as req
app = Flask(__name__)
app.secret_key = "helloFlask"

url = "http://127.0.0.1:3000/api/users?username=aaa"


dbhost = 'localhost'
dbuser = 'root'
dbpass = 'lqsym233'
dbname = 'website'
db = pymysql.connect(host = dbhost, user = dbuser, password = dbpass, database = dbname)        #連接數據庫寫法
cursor = db.cursor()                                                                            #一種轉換方法

@app.route("/")                                                             #首頁進行session判斷
def home():
    if "username" in session:                                             
        return redirect("/member")
    else:
        return render_template("front.html")

@app.route("/signin", methods=["POST"])
def judge():
    try:                                                           
        acc = request.form["x"]                                                                       #POST連線取得資料寫法
        pas = request.form["y"]
        checkacc = """SELECT * FROM user WHERE username = '%s'"""%(acc)                               #挑出與帳號相同的欄位
        cursor.execute(checkacc)                                                                      #寫入的意思 尚未commit不會有儲存動作
        r = cursor.fetchall()                                                                         #找出全部符合條件之欄位                                                                                            
        for i in r:
            username = i[2]
            password = i[3]
            name = i[1]
        print(username + "準備登入")
        if pas == password:
            session['name'] = name
            session['username'] = username
            return redirect ("/member")
        else:
            return redirect("/error/?message=帳號密碼錯誤")
    except:
        return redirect("/error/?message=帳號密碼錯誤")

@app.route("/member")
def member():
    if "username" in session:
        return render_template("correct.html", name = session['name'])
    else:
        return redirect("/")

@app.route("/error/")
def error():
    data = request.args.get("message")
    return render_template("error.html", name = data)
@app.route("/api/users")
def api():
    if "username" in session:
        username = request.args.get("username")
        checkusername = """SELECT * FROM user WHERE username = '%s'"""%(username)
        cursor.execute(checkusername)
        result = cursor.fetchall()
        if len(result) == 0:
            return json.dumps({
                    "data":None
                })
        else:
            for i in result:
                thisid = i[0]
                name = i[1]
                username = i[2]
            return json.dumps({
                    "data":{
                    "id":thisid,
                    "name":name,
                    "username":username
                    }
                }, ensure_ascii = False)
    else:
         return redirect ("/")

@app.route("/api/user", methods = ["POST"])
def apichange():
    try:
        data = request.get_json()                                                         #可以拿到以json格式傳來的資料語法 
        newusername = data["name"]
        if len(newusername) == 0:
            print(abc)
        updateusername = """UPDATE user SET name = '%s' WHERE username = '%s'"""%(newusername, session['username'])
        cursor.execute(updateusername)
        db.commit()
        changename = """SELECT * FROM user WHERE name = '%s'"""%(newusername)
        cursor.execute(changename)
        result = cursor.fetchall() 
        for i in result:
            session['name'] = i[1]
        return json.dumps({
            "ok":True
        },ensure_ascii = False)
    except:
        return json.dumps({
            "error":True
        },ensure_ascii = False)
@app.route("/signout")
def logout():
    session.pop("username", None)
    session.pop("name", None)                           #消除內容語法
    return render_template("signout.html")

@app.route("/signup/", methods = ["POST"])
def signup():
    name = request.form["n"]
    acc = request.form["a"]
    pas = request.form["p"]
    
    if name == "" or acc == "" or pas == "":
        return render_template("blank.html")
    else:
        checkname = """SELECT * FROM user WHERE username = '%s'"""%(acc)
        cursor.execute (checkname)
        result = cursor.fetchall()
        try:
            for i in result:
                n = i[2]
            print(n + "已註冊")
            return redirect("/error/?message=帳號已經有人使用") 
        except:  
                sql = """ INSERT INTO user (name, username, password) VALUES ('%s', '%s', '%s')"""%(name, acc, pas)
                cursor.execute(sql)
                db.commit()
                return render_template("oksignup.html")

        
app.run(port=3000)



