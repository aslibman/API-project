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
	page = ""
	for r in result:
		page += r + ": " + str(result[r]) + "<br>"
	return page
        #http://api.opencalais.com/enlighten/rest/
        #api for language processing

if __name__ == "__main__":
	app.debug = True
	app.run()
