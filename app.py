from flask import Flask,  redirect, render_template, request, session
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


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# taken from cs50 Pset9 finance


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
            # refusing the quest
            if request.form.get("action") == "No":
                return redirect("/ending")
        if session["steps"] == 1:
            # accepting the money
            if request.form.get("action") == "No":
                session["money"] = 10000
        if session["steps"] == 2:
            # accepting the new sword
            if request.form.get("action") == "Yes":
                session["weapon"] = "New sword"
        if session["steps"] == 3:
            # fight the dragon early
            if request.form.get("action") == "Yes":
                return redirect("/ending")
        if session["steps"] == 4:
            # went to the mountain
            if request.form.get("action") == "Yes":
                session["event1"] = True
        # first event true
        if session["event1"] == True:
            if session["steps"] == 5:
                # gave the youing dawrf money
                if request.form.get("action") == "Yes":
                    # if you don't have enough money
                    if session["money"] < 200:
                        return redirect("/ending")
                    session["money"] -= 200
                # didn't give him money
                if request.form.get("action") == "No":
                    return redirect("/ending")
            if session["steps"] == 6:
                # refused to get ore
                if request.form.get("action") == "No":
                    return redirect("/ending")
            if session["steps"] == 7:
                # fought the two orcs
                if request.form.get("action") == "Yes":
                    return redirect("/ending")
            if session["steps"] == 8:
                # used the sword to get ore
                if request.form.get("action") == "Yes":
                    # if used old sword
                    if session["weapon"] == "Old sword":
                        return redirect("/ending")
                # didn't use the sword to get the ore
                if request.form.get("action") == "No":
                    return redirect("/ending")
            if session["steps"] == 9:
                # fight the dragon
                if request.form.get("action") == "Yes":
                    session["event2"] = True
                    return redirect("/ending")
                # don't fight the dragon
                if request.form.get("action") == "No":
                    session["event2"] = False
                    return redirect("/ending")
        # first event false
        if session["event1"] == False:
            if session["steps"] == 5:
                # gave the old man food
                if request.form.get("action") == "Yes":
                    session["money"] -= 10
                    session["party"] += 1
                    session["event3"] = True
            if session["steps"] == 6:
                # fought the berserker
                if request.form.get("action") == "No":
                    # if used old sword
                    if session["weapon"] == "Old sword":
                        return redirect("/ending")
                    session["party"] += 1
                    session["event4"] = True
            if session["steps"] == 7:
                # agreed to pay the S rank
                if request.form.get("action") == "Yes":
                    # if you have enough money
                    if session["money"] >= 1000:
                        session["money"] -= 1000
                        session["party"] += 1
                        session["event5"] = True
            if session["steps"] == 8:
                # agreed to add healer to party
                if request.form.get("action") == "Yes":
                    session["party"] += 1
            if session["steps"] == 9:
                # fight the dragon
                if request.form.get("action") == "Yes":
                    session["event6"] = True
                    return redirect("/ending")
                # don't fight the dragon
                if request.form.get("action") == "No":
                    session["event6"] = False
                    return redirect("/ending")
        # move one step each choice
        session["steps"] += 1
        return redirect("/")

    # the start of the game
    if session["steps"] == 0:
        dialogue = "Hello brave hero, I am king Charles the fifth and I have summoned you here today for an important and dangerous mission. you see my daughter the princess has been kidnapped by a terrible dragon. I have already sent many troops to save her but non came back alive you are my only hope left. Do this and I will give you the hand of my only daughter in marriage and make you the heir to the throne. Do you agree?"
        return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

    if session["steps"] == 1:
        dialogue = "Thank you, brave hero, I believe that only you can save my beloved daughter, you must depart immediately for I fear that the dragon might suddenly go mad and kill my daughter. Before you go hero do you have enough money for your journey?"
        return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

    if session["steps"] == 2:
        dialogue = "If money is out of the way then do you need a new weapon to help you on your way?"
        return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

    if session["steps"] == 3:
        dialogue = "Well, then hero do you need to go on a journey to find more help or are you ready to face the dragon right now?"
        return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

    if session["steps"] == 4:
        dialogue = "if you need help I have a map here that leads you to the mountain of the dwarfs they can craft you a worthy weapon to slay a dragon with that is if you are willing to bring them something of value in return do you want to go the dwarfs?"
        return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

    # first event true
    if session["event1"] == True:

        if session["steps"] == 5:
            dialogue = "you head to the mountain of the dwarfs searching for your dragon-slaying weapon on your way there you heard that the best blacksmith in town was a dwarf named Glolvil so you went to his workshop to see if he has what you want. as you are browsing his collection of fierce-looking swords a young dwarf comes up to you and asks 'Can I help you sir?' and without waiting for you to answer he continues 'If you want to speak with the grand master I am afraid that's not possible without an appointment, but I can get you an audience with him for the low price of 200 coins, so what do you say?'"
            return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

        if session["steps"] == 6:
            dialogue = "the young dwarf leads you to the back to meet the grand master, as you enter you feel the heat rising rapidly and you see a tough-looking dwarf hammering at a sword in front of a forge when he sees you he looks at the young dwarf seemingly unhappy 'why did you bring in someone here while I am working didn't I tell you no visitors without an appointment?' 'Father this is a friend of mine that came from far away and I hope you can help him out' 'Fine what do you want and be quick I am busy' you tell the old dwarf that you want a weapon that can slay a dragon, his eyes widen and he ponders quietly before saying 'I can do that but I will need a special ore that can only be gotten from the mine west from the mountain but it's very dangerous as there is an orc clan controlling that mine and they aren't the most friendly so what do you say are you up for it?'"
            return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

        if session["steps"] == 7:
            dialogue = "you head to the mine with a drawing of the ore you need to get in hand but when you arrive there you see two orcs guarding the entrance of the mine you could try to fight them both and get through that way or you could sneak in. will you fight?"
            return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

        if session["steps"] == 8:
            dialogue = "you decide to sneak into the mine after distracting the guards with a rock you sneak in unnoticed after looking everywhere in the mine you find the ore you were looking for but it's lodged inside a wall you think you can use your sword to dislodge it but your not sure if it will be strong enough will you try?"
            return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

        if session["steps"] == 9:
            dialogue = "you got the ore thanks to your new sword you don't think your old one would have been able to dislodge the ore without breaking you return to the blacksmith to tell him the good news and he forges you a dragon-slaying sword. now you feel ready to face the dragon but will you? you can still just run away and go live a peaceful life as a farmer in another kingdom a carefree life may be waiting for you there. so what will it be will you risk your life and fight the dragon?"
            session["weapon"] = "Dragon Slayer"
            return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

    # first event false
    if session["event1"] == False:

        if session["steps"] == 5:
            dialogue = "you decide to go to the adventure guild in search of a party that can help you in defeat the dragon you on your way there you encounter an old man that asks you for some coin for his dinner do you give him?"
            return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

        # helped the old man 3rd event true
        if session["steps"] == 6 and session["event3"] == True:
            dialogue = "you gave the old man some coin for his food and he asked you if you wanted to join him as you were about to refuse you felt like you recognized this man after thinking about it you figured out that he was Merlin the best wizard in the kingdom apparently he had forgotten his coin pouch at home and he was very hungry when you asked him if he could join your party to slay the dragon he agreed and after having dinner you resumed your journey to the adventurers guild. when you arrived there it was a very noisy place and you could see a lot of potential party members but you had to find the best of the best if you wanna beat a dragon. Just when you were thinking of approaching the guild receptionist someone tripped your leg and you almost fell you looked to see who it was only to find a very buff man with firey red tattoos all over him looking at you provokingly is he challenging you? are you gonna let that slide?"
            return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

        # didn't help the old man
        if session["steps"] == 6 and session["event3"] == False:
            dialogue = "You resumed your journey to the adventurers guild when you arrived there it was a very noisy place and you could see a lot of potential party members but you had to find the best of the best if you wanna beat a dragon. Just when you were thinking of approaching the guild receptionist someone tripped your leg and you almost fell you looked to see who it was only to find a very buff man with firey red tattoes all over him looking at you provokingly is he challenging you? are you gonna let that slide?"
            return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

        # fought the berserk 4th event true
        if session["steps"] == 7 and session["event4"] == True:
            dialogue = "You decided to fight this barbarian, you are no coward you both went outside and after a hard-fought battle you managed to beat him but you recognized his strength and so after the fight, you asked him if he can join your party expecting him to refuse but surprisingly he agreed saying that he only respects the strong and that you deserved respect. you went back to the guild receptionist to ask her about the strong people in the guild and who is available, she told you that there is a rank s adventurer present in the guild but that he will only accept if you are able to pay 1000 coins as his fees."
            return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

        # didn't fight the berserk 4th event false
        if session["steps"] == 7 and session["event4"] == False:
            dialogue = "You decide to ignore the barbarian and you could hear him say coward behind you but no matter you are here for more important matters. you went back to the guild receptionist to ask her about the strong people in the guild and who is available, she told you that there is a rank S adventurer present in the guild but that he will only accept if you are able to pay 1000 coins as his fees."
            return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

        # payed for the adventurer
        if session["steps"] == 8 and session["event5"] == True:
            dialogue = "you were able to pay for such meager fees and you secured a most formidable ally. On your way out of the guild, a short woman approached you and said 'hey I heard you were looking for people to fight the dragon with I want to help you to kill that accursed beast I am a healer and I am sure I can be of help to you so what do you say can I join?'"
            return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

        # didn't pay for the adventurer
        if session["steps"] == 8 and session["event5"] == False:
            dialogue = "you couldn't pay such a price for some adventurer and decided to leave. On your way out of the guild, a short woman approached you and said 'hey I heard you were looking for people to fight the dragon with I want to help you to kill that accursed beast I am a healer and I am sure I can be of help to you so what do you say can I join?'"
            return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])

        if session["steps"] == 9:
            dialogue = "there is no more time for you to find more people the princess might be eaten at any time now will you fight the dragon with your current party?"
            return render_template("index.html", dialogue=dialogue, money=session["money"], weapon=session["weapon"], party=session["party"])


# new adventure
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
        session["event6"] = False
        session["steps"] = 0
        session["weapon"] = "Old sword"
        session["party"] = 1
        return redirect("/")
    else:
        return render_template("new_hero.html")


# endings
@app.route("/ending")
def ending():
    if session["steps"] == 0:
        dialogue = "You return back home without giving it a second thought. fight a dragon!? No way you don't want to risk your life for the princess or some throne."
        return render_template("ending.html", dialogue=dialogue)
    if session["steps"] == 3:
        dialogue = "You went to fight the dragon right away too bad you were too weak and the dragon used your bones like toothpicks. Maybe if you had a better weapon or a strong party you could have done it"
        return render_template("ending.html", dialogue=dialogue)
    # first event true
    if session["event1"] == True:
        if session["steps"] == 5:
            dialogue = "'if you can't give me the coins well then I am afraid that I can't help you, good luck.' you decide to go look for another blacksmith to forge you a weapon to defeat the dragon but you found no one capable of such a feat so you decide to try to fight the dragon as it turns out you really needed that sword as the weapon you had in hand wasn't even able to scratch the dragon and you had no way to win that fight. the dragon eats you in one bite for daring to use such a flimsy sword."
            return render_template("ending.html", dialogue=dialogue)
        if session["steps"] == 6:
            dialogue = "'if you are too afraid to fight a bunch of orcs how are you going to fight a dragon? get out of here you cowred' you were thrown out of the shop and you thought about what the old dwarf said it's true you can't even beat some orcs how are you going to defeat a dragon so you decide to go back home not face the dragon. you didn't die but no one recognized you as a hero anymore and became known as the hero who was too afired to fight an orc."
            return render_template("ending.html", dialogue=dialogue)
        if session["steps"] == 7:
            dialogue = "you decided to fight the two orcs and you were doing great at the start but when one of the guards called for help you were surrounded by hundereds of orcs and overwhelmed."
            return render_template("ending.html", dialogue=dialogue)
        if session["steps"] == 8:
            dialogue = "your old sword really couldn't hold and you were unable to get the ore, defeated you used a different ore for the weapon but when you went to fight the dragon your weapon broke and you were killed by the dragon."
            return render_template("ending.html", dialogue=dialogue)
        if session["steps"] == 9:
            # 2nd event true
            if session["event2"] == True:
                dialogue = "with your new weapon the dragon slayer in hand you went to the layer of the dragon to slay it and after a fierce battle, you were able to land a blow on the heart of the dragon killing it finally you were able to rescue the princess and become the heir to the crown you lived happily ever after with your princess and the kingdom was safe from the dragon."
                return render_template("ending.html", dialogue=dialogue)
            # 2nd event false
            if session["event2"] == False:
                dialogue = "why should you risk your life for a princess you don't know? you decide to flee the kingdom to start a new life as a farmer. years passed and you heard that the kingdom was regularly attacked by that dragon it's none of your business though you are living just fine on your farm."
                return render_template("ending.html", dialogue=dialogue)
    # first event false
    if session["event1"] == False:
        if session["steps"] == 6:
            dialogue = "you tried to teach this barbarian a lesson but while you were fighting him your old sword broke causing you to embarrass yourself you were so ashamed that you ran out of the guild and never showed up again in fact you were so embarrassed you gave up your quest and lived in shame the end."
            return render_template("ending.html", dialogue=dialogue)
        if session["steps"] == 9:
            # 6th event true
            if session["event6"] == True:
                if session["party"] < 3:
                    dialogue = "you went to fight the dragon but you didn't have enough party members to be able to defeat the dragon, in the end, you were defeated and the dragon made a barbecue out of you."
                    return render_template("ending.html", dialogue=dialogue)
                if session["party"] == 3:
                    dialogue = "you went to fight the dragon with your party of three you all fought the dragon for three days and three nights and by the end of it you were the last one standing you defeated the dragon but at what cost you lost two comrades that day but you saved the princess and become the heir of the crown you never did forget your comrades but life goes on."
                    return render_template("ending.html", dialogue=dialogue)
                if session["party"] == 4:
                    dialogue = "you went to fight the dragon with your party of four you all fought the dragon and you managed to beat it with no casualties but you lost your arm in the process while protecting your comrades even though you saved the princess you can't fight anymore due to your arm not that you will need to when you become the king."
                    return render_template("ending.html", dialogue=dialogue)
                if session["party"] == 5:
                    dialogue = "you went to fight the dragon with your party of five you all fought the dragon and you managed to beat it with no casualties in fact your party was so strong no one was injured too badly you rescued the princess and the legend of your party will be told for generations as the heroes who beat a dragon with ease."
                    return render_template("ending.html", dialogue=dialogue)
            # 6th event fasle
            if session["event6"] == False:
                dialogue = "you went to look for more party members but by the time you were satisfied you heard the news of the princesse being eaten you failed to save her because you wasted too much time."
                return render_template("ending.html", dialogue=dialogue)
