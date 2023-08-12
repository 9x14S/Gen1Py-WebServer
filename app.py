from flask import Flask, render_template, request, redirect

app = Flask(__name__) # Turn this file into a Flask app

# Python Decorator assigns the below function to the assigned route.
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
	if 'file' in request.files:
		file = request.files['file']
		return "Succesfully caught a file."
	else:
		return "Didn't get a file. <a href='/'>Go back</a>"

@app.route("/edit", methods=["GET", "POST"])
def edit():
	if request.method=="GET":
		return redirect("/")
		# don't let users go straight to the edit page without a save file.
	elif request.method=="POST":
		# TODO: add file validation and an intermediate path.
		playername="test_name", 
		money="test_money", 
		playerid=-1, 
		firstpokename="test_pokename"
		return render_template("edit_page.html", 
									playername=playername, 
									money=money, 
									playerid=playerid, 
									firstpokename=firstpokename
									)