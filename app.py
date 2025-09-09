from flask import Flask, render_template, request
import requests
app = Flask (__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/emojis")
def emojis():
    query = request.args.get("q","")
    category = request.args.get("category","")
    sort = request.args.get("sort","")

    if query:
        url = f"https://emojihub.yurace.pro/api/search?q={query}"
    elif category:
        url = f"https://emojihub.yurace.pro/api/all/category/{category}"
    else:
        url = "https://emojihub.yurace.pro/api/all"

    try:
        response = requests.get(url)
        response.raise_for_status()
        emojis = response.json()
    except Exception as e:
        print("Ошибка при запросе API:",e)
        emojis = []

    if sort == "asc":
        emojis = sorted(emojis, key=lambda e: e["name"])
    elif sort == "desc":
        emojis = sorted(emojis, key=lambda e: e["name"], reverse = True)


    return render_template("emojis.html", emojis=emojis)

import os
if __name__=="__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port,debug=True)
