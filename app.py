from Python.printhex import hex_dump, translate 
from Python.wrapper import *
from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os
app = Flask(__name__) # Turn this file into a Flask app


# Some configuration
ALLOWED_EXTENSIONS = ["sav"]
UPLOAD_FOLDER = "Uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 33 * 1024 # Set the maximum file size to 32KB + 1KB

# Extra function I stole from Flask's documentation
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Python Decorator assigns the below function to the assigned route.
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    # Check if there's actually a file uploaded 
    if 'savefile' in request.files and request.files["savefile"].filename != '':
        return redirect("/parse", code=307)
    else:
        return redirect("/")

@app.route("/parse", methods=["POST"])
def parse():
    # TODO: call the Gen1Py functions to read the uploaded file and pass back savefile info. 
    savefile = request.files['savefile']
    if savefile and allowed_file(savefile.filename): # Save the file to /Uploads
        filename = secure_filename(savefile.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        savefile.save(filepath)
        
        
        unformatted_name = hex_dump(filepath, 'name')
        formatted_name = translate(unformatted_name)
        
        
        return redirect("/edit", code=307)
    
    return redirect("/")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method=="GET":
        return redirect("/") # Don't let users go straight to the edit page without a save file.
        
    elif request.method=="POST":
        # I made a mess here, sorry
        # TODO: 
        # I should make some extra functions to get all the info at the same time and 
        # parse it instead of doing this 
        
        savefile=secure_filename(request.files['savefile'].filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], savefile)

        unformatted_name = hex_dump(filepath, 'name')
        formatted_name = translate(unformatted_name)

        playername = formatted_name
        money = ''.join([x.removeprefix("0x") for x in map(hex, hex_dump(filepath, 'money'))])
        money = money.removeprefix('0')
    
        # This is tricky, as I can't view the player's id ingame
        playerid = ''.join(map(str, hex_dump(filepath, "id")))
        firstpokename = "test_pokename"
        return render_template("edit_page.html", 
                                savefile=savefile,
                                playername=playername, 
                                money=money, 
                                playerid=playerid, 
                                firstpokename=firstpokename
                                )

#test
@app.route("/save", methods=["POST"])
def save():
    savefile=request.headers.get('savefile', "")
    playername=request.headers.get('playername', "")
    money=request.headers.get('money', "")
    playerid=request.headers.get('playerid', "")
    firstpokename=request.headers.get('firstpokename', "")
    #TODO: Put your compilation functions here.
    testfile_directory=UPLOAD_FOLDER
    testfile_path=savefile
    return send_from_directory(directory=testfile_directory, path=testfile_path)