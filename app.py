from flask import Flask, render_template, request

app = Flask(__name__) # Turn this file into a Flask app

# Python Decorator assigns the below function to the assigned route.
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/edit")
def edit():
	return render_template("edit_page.html", playername="test_name", money="test_money", playerid=-1, firstpokename="test_pokename")