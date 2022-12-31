import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from functools import wraps

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///history.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("hero_name") is None:
            return redirect("/new_hero")
        return f(*args, **kwargs)
    return decorated_function


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"), ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        if session["steps"] == 0:
            if request.form.get("action") == "No":
                return redirect("/ending")
        if session["steps"] == 1:
            if request.form.get("action") == "No":
                session["money"] = 10000
        if session["steps"] == 2:
            if request.form.get("action") == "Yes":
                session["weapon"] = "New sword"
        if session["steps"] == 3:
            if request.form.get("action") == "Yes":
                return redirect("/ending")
        session["steps"] += 1
        return redirect("/")

    if session["steps"] == 0:
        dialogue = "Hello brave hero, I am king Charles the fifth and I have summoned you here today for an important and dangerous mission.\n you see my daughter the princess has been kidnapped by a terrible dragon.\n I have already sent many troops to save her but non came back alive you are my only hope left.\n Do this and I will give you the hand of my only daughter in marriage and make you the heir to the throne. Do you agree?"
        return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"])
    if session["steps"] == 1:
        dialogue = "Thank you brave hero, I belive that only you can save my beloved daughter, you must depart immedaitly for I fear that the dragon might suddnely go mad and kill my daughter. Before you go hero do you have enough money for your journee?"
        return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"])
    if session["steps"] == 2:
        dialogue = "if money is out of the way then do you need a new weapon to help you on your way?"
        return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"])
    if session["steps"] == 2:
        dialogue = "if money is out of the way then do you need a new weapon to help you on your way?"
        return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"])
    if session["steps"] == 3:
        dialogue = "Well then hero do you need to go on a journee to find more help or are you ready to face the dragon right now?"
        return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"])


@app.route("/new_hero", methods=["GET", "POST"])
def new_hero():
    if request.method == "POST":
        # Forget any user_id
        session.clear()
        if not request.form.get("username"):
            return apology("must provide Hero Name", 400)
        session["hero_name"] = request.form.get("username")
        session["money"] = 100
        session["event1"] = False
        session["event2"] = False
        session["event3"] = False
        session["event4"] = False
        session["event5"] = False
        session["steps"] = 0
        session["weapon"] = "Old sword"
        return redirect("/")
    else:
        return render_template("new_hero.html")


@app.route("/ending")
def ending():
    if session["steps"] == 0:
        dialogue = "You return back home without givving it a second thoght. fight a dragon!? No way you don't want to risk your life for the princess or some throne"
        return render_template("ending.html", dialogue=dialogue)
    if session["steps"] == 3:
        dialogue = "You went to fight the dragon right away too bad you were too weak and the dragon used your bones like toothpicks. Maybe if you had a better weapon or a strong party you could have done it"
        return render_template("ending.html", dialogue=dialogue)
