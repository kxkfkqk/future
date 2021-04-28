from flask import request
from flask import Flask
import json
import pymysql
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

db = pymysql.connect(host = "localhost", user = "root", password = "Lqsym233!", database = "website")
cursor = db.cursor()

# Pages test
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")
@app.route("/api/attractions")
def attractions():
	alldata = []
	end = 12
	page = int(request.args.get("page"))
	nextpage = page + 1
	page = (page*12) + 1

	if page >=313:
		nextpage = None
		end = 7
	if page > 324:
		return json.dumps({
				"error":True,
				"message":"資料錯誤"
			},ensure_ascii = False)
	keyword = request.args.get("keyword")

	if keyword == None:
		try:
			for j in range(page, (page + end)):
				imgages = []
				url = """SELECT * FROM img WHERE no = '%s'"""%(j)
				cursor.execute(url)
				results = cursor.fetchall()
				for k in results:
					img = [k[2]]
					imgages += img
				da = """SELECT * FROM data WHERE id ='%s'"""%(j)
				cursor.execute(da)
				result = cursor.fetchall()
				for i in result:
					ide = i[0]
					name = i[1]
					category = i[2]
					description = i[3]
					address = i[4]
					transport = i[5]
					mrt = i[6]
					latitude = i[7]
					longitude = i[8]
					data  = [{
							"id":ide,
							"name":name,
							"category":category,
							"description":description,
							"address":address,
							"transport":transport,
							"mrt":mrt,
							"latitude":latitude,
							"longitude":longitude,
							"imgages":imgages
						}]
					alldata += data
			return json.dumps({
				"nextPage":nextpage,
				"data":alldata
			},ensure_ascii = False)
		except:
			return json.dumps({
				"error":True,
				"message":"資料錯誤"
			},ensure_ascii = False)

	else:
		try:
			count = -1
			keyword = "%" + keyword + "%"
			da = """SELECT * FROM data WHERE name LIKE '%s'"""%(keyword)
			cursor.execute(da)
			result = cursor.fetchall()
			for i in result:
				count += 1
				ide = i[0]
				name = i[1]
				category = i[2]
				description = i[3]
				address = i[4]
				transport = i[5]
				mrt = i[6]
				latitude = i[7]
				longitude = i[8]
				imgages = []
				url = """SELECT * FROM img WHERE no = '%s'"""%(ide)
				cursor.execute(url)
				res = cursor.fetchall()
				for j in res:
					img = [j[2]]
					imgages += img
				data  = [{
						"id":ide,
						"name":name,
						"category":category,
						"description":description,
						"address":address,
						"transport":transport,
						"mrt":mrt,
						"latitude":latitude,
						"longitude":longitude,
						"imgages":imgages
					}]
				alldata += data
			if count  <= (page + 10):
				nextpage = None
			if count < (page - 1):
				return json.dumps({
					"error":True,
					"message":"資料錯誤"
				},ensure_ascii = False)
			else:
				return json.dumps({
					"nextPage":nextpage,
					"data":alldata[(page - 1):(page + 11)]
				},ensure_ascii = False)
		except:
			return json.dumps({
					"error":True,
					"message":"資料錯誤"
				},ensure_ascii = False)
	

@app.route("/api/attraction/<number>")
def attractions2(number):
	x = []
	try:
		url = """SELECT * FROM img WHERE NO = '%s'"""%(number)
		cursor.execute(url)
		results = cursor.fetchall()
		for k in results:
			imgages = [k[2]]
			x = x + imgages
		sql = """SELECT * FROM data WHERE id = '%s'"""%(number)
		cursor.execute(sql)
		result = cursor.fetchall()
		for i in result:
			ide = i[0]
			name = i[1]
			category = i[2]
			description = i[3]
			address = i[4]
			transport = i[5]
			mrt = i[6]
			latitude = i[7]
			longitude = i[8]
			data  = [{
					"id":ide,
					"name":name,
					"category":category,
					"description":description,
					"address":address,
					"transport":transport,
					"mrt":mrt,
					"latitude":latitude,
					"longitude":longitude,
					"imgages":x
				}]
		return json.dumps({
					"data":data
				},ensure_ascii = False)
	except:
		return json.dumps({
			"error":True,
			"message":"資料錯誤"
		},ensure_ascii = False)
app.run(host = "0.0.0.0", port=3000)
