"""
Flask app file. Run with 'python(3) -m Flask run' after activating the virtual environment.

This program starts a local webserver that enables you to open a Gen 1 Pokémon save file, and
    to view or edit it. 
    
This program carries no warranty whatsoever. If you use it, you're responsible for any damages to your 
    save. We can't help you if you mess your save file by doing dumb editions.
    
    Research well before making any editions. 
    
Made by 9x14S and Micah Raney.
"""

from Package import * 
from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
app = Flask(__name__) # Turn this file into a Flask app


# Some configuration
ALLOWED_EXTENSIONS = ["sav"]
UPLOAD_FOLDER = "Uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 33 * 1024 # Set the maximum file size to 32KB + 1KB


# Python Decorator assigns the below function to the assigned route.
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    # Check if there's actually a file uploaded 
    if 'savefile' in request.files and request.files["savefile"].filename != '':
        return redirect("/edit", code=307)
    return redirect("/")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method=="GET":
        return redirect("/", code=303) # Don't let users go straight to the edit page without a save file.
        
    elif request.method=="POST":
        savefile = request.files['savefile']

        # Save the file to /Uploads
        try:
            if savefile and allowed_file(savefile.filename): 
                filename = secure_filename(savefile.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                savefile.save(filepath)
            
                # Open the file and extract the data as a dictionary
                with open(filepath, 'rb') as file:
                    save = SaveFile(file.read())
                    data, badges_owned = save.extract_data()
                    
                # Render the template with the extracted data 
                return render_template("edit_page.html", 
                                        data=data,
                                        savefile=filename,
                                        badges_owned=badges_owned,
                                        badges=BADGE_DICT,
                                        data_names=DATA_NAMES,
                                        data_tips=DATA_TIPS
                )
        except Exception:
            # If something went wrong, render the error page
            return render_template("error_page.html")

@app.route("/download", methods=["GET", "POST"])
def download_file(): 
    # Editing has been done and file is to be sent
    
    if request.method == "GET":
        return redirect("/", code=303)
    
    elif request.method == "POST":
        filepath = secure_filename(request.form.get("filepath"))
        try: 
            # Open the file, read the data, compare it and then write the data
            # supplied by the form into it
            path_with_folder = os.path.join(app.config["UPLOAD_FOLDER"], filepath)
            with open(path_with_folder, "r+b") as savefile:
                file_data = bytearray(savefile.read())
                save_data = SaveFile(file_data)
                data_dict = request.form.to_dict(flat=False)
                savefile.seek(0, 0)
                savefile.write(save_data.write_data(data_dict))
                total_checksum = checksum(file_data)
                savefile.seek(0x3523, 0)
                savefile.write(total_checksum)
        except FileNotFoundError as e:
            print(e) 
            return render_template("error_page.html")
            
        return send_from_directory(app.config['UPLOAD_FOLDER'], filepath)


# Extra function I stole from Flask's documentation
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
