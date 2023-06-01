import json
from sys import argv
from colorama import *

'''
class Pokemon():
    def __init__(self):
        try:
            with open("pkmn.json", "r") as p:
                data = p.read()
        except Exception:
            print("An error ocurred while importing Pokemon data. ")
            exit(1)
'''

def edit_hex(hexdata, offset:bytes, val:bytes, hex=True):
    with open(argv[1].split(".")[0] + " (modified).sav","wb") as saveoutput:
        try:
            hexdata[offset] = val
            """             
            if hex:
            offset = int(edt, base=16)
            hexdata[offset] = int(val.capitalize(), base=16)
            else:
            offset = int(edt)
            hexdata[offset] = int(val) 
            """
            saveoutput.write(hexdata)
            return 
        except Exception as e:print(f"hex_E; {e}")

# Function to compute the checksum needed so that the save doesn't appear corrupted in the game
def checksum(data): 
    # Initilize the checksum variable to 255, then subtract from each each value from the range
    total_checksum = bytes(255)
    for i in data[9624:13602+1]:
        total_checksum -= i
    # Then inject it back to its place
    if (total_checksum < 0):
        total_checksum = 0
    data[13603] = total_checksum
    
def open_file():
    with open(argv[1], "rb") as f:
        hexdata = bytearray(f.read())
    return hexdata

# Function to print the selected bank of data to the screen
def print_hexdata(hexdata:bytearray):
    
    # Ignore these two functions, they're colorama's
    just_fix_windows_console()
    init(autoreset=True)
    
    # Get the bank to print from the user and the byte width
    choice = int(input("Select bank to view (0, 1, 2, 3): "))
    bytes_to_print = int(input("Type in the number of bytes to display: "))
    # Select the bank 
    match (choice):
        case 0:
            bank = range(0, 8191)
        case 1:
            bank = range(8192, 16383)
        case 2:
            bank = range(16384, (16384 * 2) - 1)
        case 3:
            bank = range(16384 * 2, 16384 * 4 - 1)
        
    # count is the variable that determines if a newline should be printed 
    # data_string is a placeholder for the bytes' potential meaning before it is printed
    count = 1
    data_string = ""
    print("Printing Hex Data...\n", "-" * 105)
    
    # Start of loop, it loops over every byte in the bank selected
    for t in bank:
        
        # If the current byte is a printable ASCII character, add it to data_string
        if ((hexdata[t] > 31 ) and (hexdata[t]) < 127):
            # If the current character is a period, then print it with color green to differentiate
            # between it and the placeholder periods used for non-printable characters
            if (chr(hexdata[t]) == "."):
                data_string += Fore.GREEN + (chr(int(hexdata[t])))
            else:
                data_string += chr(int(hexdata[t]))
        
        # If not a printable character, then add a period
        else:
            data_string += "."
            
        # hex_string contains the bytes as they are represented in hexadecimal
        # It is also right-justified for even printing
        hex_string = (hex(hexdata[t])).rjust(5, " ")
        
        # If count equals the byte width, then print WITH a newline and reset count, otherwise print without
        # and increment count
        if (count == bytes_to_print):
            print(hex_string, f"# {data_string}")
            data_string = ""
            count = 0
        else:
            print(hex_string, end="")
        count += 1
    print("\n\r", "-" * 105)