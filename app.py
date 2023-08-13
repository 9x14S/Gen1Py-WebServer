"""
Flask app file. Run with 'python(3) -m Flask run' after activating the virtual environment.

This program starts a local webserver that enables you to open a Gen 1 Pokémon save file, and
    to view or edit it. 
    
This program carries no warranty whatsoever. If you use it, you're responsible for any damages to your 
    save. We can't help you if you mess your save file by doing dumb editions.
    
    Research well before making any editions. 
    
Made by 9x14S and Micah Raney.
"""

import os

from Package import * 
from flask import Flask, render_template, request, redirect

from werkzeug.utils import secure_filename
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
        
        return redirect("/edit", code=307)
    
    return redirect("/")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method=="GET":
        return redirect("/") # Don't let users go straight to the edit page without a save file.
        
    elif request.method=="POST":
        
        savefile=secure_filename(request.files['savefile'].filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], savefile)
        
    # Open the file and extract the data as a dictionary
    with open(filepath, 'rb') as file:
        openfile = file.read()
        data = extract_data(openfile)

    return render_template("edit_page.html", 
                            savefile=savefile,
                            playername=data['name'], 
                            money=data['money'], 
                            playerid=data['id'], 
                            firstpokename='bbb' # Have to change
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

  
# Extra function I stole from Flask's documentation
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
