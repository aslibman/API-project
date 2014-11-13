from flask import Flask, render_template, redirect, session, url_for, request 
import json, urllib2, urllib, unirest

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
        request1 = urllib2.urlopen(url)
        result = json.loads(request1.read())
        if len(result) < 2:
                return redirect(url_for("index"))
        result["ChangePercent"] = str(result["ChangePercent"])[:4]

        #Google News
        name = "_".join(result["Name"].split(" ")[:-1])
        name = urllib.quote(name)
        print name
        url = "https://ajax.googleapis.com/ajax/services/search/news?v=1.0&q=%s"%name
        firstBundle = getNews(url)
        newsForApp = firstBundle[0]
                
        
        
        #Facebook
##      url = "https://graph.facebook.com/search?access_token=CAACEdEose0cBAMrNZBTDulP8sNNvYTS7zo7fHoRie3d8rK83MJAMI1E7oHgwLaXbHUGDkdFYsZBFoWqq7zoiYGVQWn9hVgZAMfw7w1bT8H6bjMcJD01t7dKef3PLQ0BAZADcVM7lDMy7QlLJTSq19LGSCLtfGLQEVlA8ADNGsDFISTjQBjkbYh0q3UYpuFoNeAPoX86QYFfSe39zK4sZB&q=%s&type=post"%name
##      request3 = urllib2.urlopen(url)
##      facebook = json.loads(request3.read())["data"]
##      facebookText = []
##      for r in facebook:
##              if "description" in r:
##                      facebookText.append(r["description"])
##              elif "caption" in r:
##                      facebookText.append(r["caption"])

        return render_template("lookup.html",info=result,news=newsForApp)

def getNews(url):
	request2 = urllib2.urlopen(url)
	request2 = json.loads(request2.read())
	news = request2["responseData"]["results"]
	#getting Sentiment
	newsForApp = []
	for r in news:
		entry = {}
		entry['unescapedUrl']=r['unescapedUrl']
		entry['titleNoFormatting'] = r['titleNoFormatting']
		url = entry['unescapedUrl']
		response = unirest.get("https://loudelement-free-natural-language-processing-service.p.mashape.com/nlp-url/?url=%s"%url,headers={"X-Mashape-Key": "ef5Dv9PwnYmshcMGgQi24Ki0WZKUp1jKZIrjsnemrdgI9ShNW2"})
		response = json.loads(response.raw_body)
		if 'sentiment-text' in response:
			entry['sentType'] =  response['sentiment-text']
			entry['sentNum'] = abs(float(response['sentiment-score']) * 100)
		else:
			entry['sentType'] = "no result"
			entry['sentNum'] = 0
		newsForApp.append(entry)
	nextUrl = request2["responseData"]["cursor"]["moreResultsUrl"]
	return (newsForApp,nextUrl)

if __name__ == "__main__":
        app.debug = True
        app.run()
