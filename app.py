from flask import Flask, render_template, request, redirect

app = Flask(__name__) # Turn this file into a Flask app

# Python Decorator assigns the below function to the assigned route.
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
	if 'savefile' in request.files:
		return redirect("/parse", code=307)
	else:
		return "Didn't get a file. <a href='/'>Go back</a>"

@app.route("/parse", methods=["POST"])
def parse():
	# TODO: call the Gen1Py functions to read the uploaded file and pass back savefile info. 
	savefile = request.files['savefile']
	return redirect("/edit", code=307)

@app.route("/edit", methods=["GET", "POST"])
def edit():
	if request.method=="GET":
		return redirect("/")
		# don't let users go straight to the edit page without a save file.
	elif request.method=="POST":
		savefile=request.files['savefile']
		# TODO: add file validation and an intermediate path.
		playername="test_name", 
		money="test_money", 
		playerid=-1, 
		firstpokename="test_pokename"
		return render_template("edit_page.html", 
									savefile=savefile,
									playername=playername, 
									money=money, 
									playerid=playerid, 
									firstpokename=firstpokename
									)