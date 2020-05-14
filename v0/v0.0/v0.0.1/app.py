from flask import Flask, request, render_template, redirect, send_file, jsonify, url_for, g, session
import json
from threading import Thread
from requests_oauthlib import OAuth2Session
import os

app = Flask("")

base_url = "https://cafe.seba.gq"

os.environ["OAUTH2_CLIENT_ID"] = os.environ.get("OAUTH2_CLIENT_ID")
os.environ["OAUTH2_CLIENT_SECRET"] = os.environ.get("OAUTH2_CLIENT_SECRET")

OAUTH2_CLIENT_ID = os.environ['OAUTH2_CLIENT_ID']
OAUTH2_CLIENT_SECRET = os.environ['OAUTH2_CLIENT_SECRET']
OAUTH2_REDIRECT_URI = 'http://cafe.seba.gq/callback'

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET

if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

def token_updater(token):
    session['oauth2_token'] = token

def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)

@app.route('/login')
def login():
    scope = request.args.get(
        'scope',
        "identify")
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    if request.values.get('error'):
        return request.values['error']
    discord = make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorization_response=request.url)
    session['oauth2_token'] = token
    return redirect("/")

@app.route("/<story>")
def stories(story):
    
    with open("data/stories.json", "r") as f:
        l = json.load(f)

    try:
        title = l[str(story)]["title"]
        story = l[str(story)]["file"]
  
    except KeyError:
        return "Story not found"

    file = open(f"data/stories/{story}", "r")
    f = file.read()
    file.close()

    f = f.replace("\n", "<br>")

    return render_template("story.html", title = title, story = f, author = "bruh")

@app.route("/post", methods = ["GET", "POST"])
def post():

    if request.method != "POST":
        return render_template("post.html")

    else:
        title = request.form["title"]
        story = request.form["story"]

        input = f"\"post {title} | {story}"

        return render_template("post_done.html", input = input)

@app.route("/")
def index():
  try:
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    nickname = user["username"] + "#" + user["discriminator"]

  except KeyError:
    return render_template("index_no_login.html")

  return render_template("index.html", user = nickname)
    
@app.route("/stories")
def stories_list():
  with open("data/stories.json") as f:
    l = json.load(f)

  dict_keys = l.keys()
  dict_keys = [a for a in dict_keys]
  dict_keys.sort()

  stories = {}

  for a in dict_keys:
    stories[a] = l[a]

  return render_template("stories.html", stories = stories)

def run():
    app.run(host="0.0.0.0")

def run_app():  
    t = Thread(target=run)
    t.start()