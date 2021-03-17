from flask import Flask
from flask import request
from flask import redirect
import json
from flask import render_template
from flask import session
app=Flask(__name__)
app.secret_key="helloFlask"


@app.route("/")
def home():
    if "username" in session:
        return redirect("/member/")
    else:
        return render_template("front.html")
@app.route("/signin", methods=["POST"])
def judge():
    acc=request.form["x"]
    pas=request.form["y"]
    if acc == "test" and pas == "test":
        session['username'] = "hi"
        return redirect ("/member/")
    else:
        return redirect ("/error/")
@app.route("/member/")
def member():
    if "username" in session:
        return render_template("correct.html")
    else:
        return redirect("/")
@app.route("/error/")
def error():
    return render_template("error.html")
@app.route("/signout")
def logout():
    session.pop("username", None)
    return render_template("signout.html")
app.run(port=3000)