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
Once the above steps are completed, run the command `flask run` in the Gen1Py directory. This should activate a Flask webserver and spit out an ip and port number (ex. 127.0.0.1:5000). Navigate to this address in your browser to use the webapp locally, or configure it for your own hosted use. 

## To-Do

+ [x] A function for printing the data inside a save

  + An option to export the printed data to a file
+ [ ] Better color printing. Maybe not?

+ [ ] Linux/MacOS compatibility

+ [ ] Logging for online use with `logging`

+ [ ] Support for other localizations and games in the generation (Yellow)

+ [ ] Command Line argument parsing with `argparse`. So that the input() functions can be dropped

  + [ ] "help"/--help/-h flag comprehension. If using a flag, override all others including the command
  + [ ] "print" command comprehension to format and print the save file
    + [ ] -f/--full flag for printing/exporting all the data (exclusive with -b and -o)
    + [ ] -F/--no-format to print the data as-is, without any formatting (default: hex)
    + [ ] -b/--bank (bank) flag + number between 0-3 to print/export the selected bank (exclusive with -f and -o)
    + [ ] -o/--offset (offset) flag + offset to print the hex value at that offset (exclusive with -b and -f)
    + [ ] -e/--export [filename] flag for exporting the print to a file. If the file name is omitted, def ault to the name of the source file plus an added "(exported)".
    + [ ] -H/--hex/-d/--decimal flags for printing/exporting in hexadecimal or decimal
    + [ ] -v/--verbose flag to print every action (for debugging, should use the `logging` module)
  + [ ] "edit" command to edit a value or values
    + [ ] -j/--json (file) to import the values to be replaced from a .json file
    + [ ] -o/--offset (offset) flag + offset to edit the hex value at that offset
    + [ ] -p/--print to edit and print the change and the checksum if it is not silenced (the default)
    + [ ] -n/--no-print to simply edit and not print anything
    + [ ] -c/--checksum to compute the checksum and edit its value (the default)
    + [ ] -N/--no-checksum to not compute or edit its value
    + [ ] -v/--verbose flag to print every action (for debugging)
    + [ ] command shortcuts like "name" or "money" + [value] to quickly edit variables in the save

## Similar Projects or Posibilities to Expand

+ [ ] Maybe a GUI version

+ [ ] Maybe create a PyPi Package out of this

+ [ ] A way to import the data from the Pokemon Showdown export option

### Current goal

+ [ ] A simple online version so that nothing has to be downloaded/installed
