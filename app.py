from flask import Flask, render_template, request
import json
from threading import Thread

app = Flask("")

@app.route("/")
def index():
    return '<h1 style="text-align:center">BRUH</h1>'

@app.route("/<story>")
def stories(story):
    
    with open("data/stories.json", "r") as f:
        l = json.load(f)

    try:
        story = l[str(story)]["file"]
    except KeyError:
        return "Story not found"

    file = open(f"data/stories/{story}", "r")
    f = file.read()
    file.close()

    f = f.replace("\n", "<br>")

    return f     

@app.route("/post", methods = ["GET", "POST"])
def post():

    if request.method != "POST":
        return render_template("post.html")

    else:
        title = request.form["title"]
        story = request.form["story"]

        input = f"\"post {title} | {story}"

        return render_template("post_done.html", input = input)

def run():
    app.run(host="0.0.0.0")

def run_app():  
    t = Thread(target=run)
    t.start()