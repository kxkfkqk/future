from flask import Flask
from flask import request
from flask import redirect
import json
from flask import render_template
from flask import session
import pymysql
app = Flask(__name__)
app.secret_key = "helloFlask"

dbhost = 'localhost'
dbuser = 'root'
dbpass = 'lqsym233'
dbname = 'website'
db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)        #連接數據庫寫法
cursor = db.cursor()                                                                    #一種轉換方法

@app.route("/")                                         
def home():
    if "username" in session:                                             
        return redirect("/member")
    else:
        return render_template("front.html")

@app.route("/signin", methods=["POST"])
def judge():                                                           
    acc = request.form["x"]                                                                       #POST連線取得資料寫法
    pas = request.form["y"]
    checkacc = """SELECT * FROM user WHERE username = '%s'"""%(acc)                               #挑出與帳號相同的欄位
    cursor.execute(checkacc)                                                                      #寫入的意思 尚未commit不會有儲存動作
    r = cursor.fetchall()                                                                         #找出全部符合條件之欄位
    try:                                                                                            
        for i in r:
            username = i[2]
            password = i[3]
            name = i[1]
        print(username)
        if pas == password:
            session['username'] = name
            return redirect ("/member")
        else:
            return redirect("/error/")
    except:
        return redirect("/error/")

@app.route("/member")
def member():
    if "username" in session:
        return render_template("correct.html", name = session['username'])
    else:
        return redirect("/")

@app.route("/error/")
def error():
    return render_template("error.html")

@app.route("/signout")
def logout():
    session.pop("username", None)
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
            print(n)
            return render_template("signuperror.html") 
        except:  
                sql = """ INSERT INTO user (name, username, password) VALUES ('%s', '%s', '%s')"""%(name, acc, pas)
                cursor.execute(sql)
                db.commit()
                return render_template("oksignup.html")

        
app.run(port=3000)



