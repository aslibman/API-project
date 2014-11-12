from flask import Flask, render_template, redirect, session, url_for, request 
import json, urllib2

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
	if request.method == "GET":
		return render_template("index.html")
	else:
		return redirect("/s/" + request.form["ticker"])

@app.route("/s/")
@app.route("/s/<stock>")
def lookup(stock = "GOOG"):
	url = "http://dev.markitondemand.com/Api/v2/Quote/json?symbol=%s&callback=myFunction"%stock
	request = urllib2.urlopen(url)
	result = json.loads(request.read())
	if len(result) < 2:
		return redirect(url_for("index"))
	result["ChangePercent"] = str(result["ChangePercent"])[:4]
	
	#Google News
	name = result["Name"].split(" ")[0]
	url = "https://ajax.googleapis.com/ajax/services/search/news?v=1.0&q=%s"%name
	request = urllib2.urlopen(url)
	news = json.loads(request.read())["responseData"]["results"]

	return render_template("lookup.html",info=result,news=news)

if __name__ == "__main__":
	app.debug = True
	app.run()
