# Gen1Py

A simple Pokemon Save File Editor for the Generation 1 games (Red, Green, Blue and (not yet) Yellow)

## Installation

### Windows:
Make sure you have `python-virtualenv` installed through `pip` and `GCC`.

Then change directory into this folder and run `make`, activate the virtual environment that was just made and type `make install` to install the required `pip` packages. That's it! Congrats.

### POSIX:
Make sure you have the `python3-virtualenv` package installed with your OS's package manager (not `pip`) and `GCC`.

Then type `make`, afterwards, `cd` into the folder and activate the virtual environment. Finally, type `make install` to install the required `pip` packages. Congratulations! We're so happy for you.

#### Web Interface:
Once the above steps are completed, run the command `python -m flask run` (Windows) or `python3 -m flask run` (POSIX) in the Gen1Py directory. This should activate a Flask webserver and spit out an IP and port number (ex. 127.0.0.1:5000). Navigate to this address in your browser to use the webapp locally, or configure it for your own hosted use. 

## To-Do

+ [x] A function for printing the data inside a save

+ [ ] Better design the webpages

+ [ ] Make the code less of a mess

+ [ ] Linux/MacOS/Windows compatibility

+ [ ] Support for other localizations and games in the generation (Yellow)

+ [ ] Add more editing options.

## Posibilities to Expand

+ [ ] A way to import the data from the Pokemon Showdown export option
      
+ [ ] A GUI, or maybe making it a command line tool.
      
+ [ ] Adding more support for Gen 1.
      
+ [ ] Adding support for other generations.

