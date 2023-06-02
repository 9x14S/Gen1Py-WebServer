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

# Function to edit the memory addresses
def edit_hex(hexdata, offset, val:bytes) -> None:
    
    # Open both files, the source and the output file
    with open(file=argv[1].split(sep=".")[0] + " (modified).sav", mode="wb") as saveoutput:
        
        # Exception handling for any incorrect values
        try:
            
            # Save the previous value for later printing. Then replace the offset with the value
            prev_val = hexdata[offset]
            hexdata[offset] = val
            print(f"Edition done at offset {hex(offset)}, with '{prev_val}' replaced with '{hexdata[offset]}'.")
            saveoutput.write(checksum(hexdata))
            return 
        
        # If an exception happens, then exit
        except Exception as e:
            print(f"edit_hex_E; {e}")
            print("Exiting...")
            exit(code=1)

# Function to compute the checksum needed so that the save doesn't appear corrupted in the game
'''The checksum is calculated as follows:
Initialize the checksum byte to 0.
Binary sum the values in each memory address from 0x2598 to 0x3522 exclusive, ignoring any carryover.
Invert the result.

Then the checksum result is inserted at (decimal) offset 13603 to be compared while running.'''
def checksum(data:bytearray) -> bytearray: 
    # Initialize the checksum variable to 0, then add to it each value from the range
    total_checksum = bytearray(1)
    for i in data[0x2598:0x3522]:
        if ((total_checksum[0] + i) > 255):
            temp = int(total_checksum[0])
            total_checksum[0] = (temp + i) - 255
        else:
            total_checksum[0] += i
    # Then, invert it and inject it back to its place
    total_checksum[0] ^= 0xFF
    print(f"Checksum value: {total_checksum[0]}")
    data[13603] = total_checksum[0]
    return data
    
# Function to open the save file and return it as a bytearray object
def open_file() -> bytearray:
    with open(argv[1], "rb") as f:
        hexdata = bytearray(f.read())
    return hexdata

# Function to print the selected bank of data to the screen
def print_hexdata(hexdata:bytearray) -> None:
    
    # Ignore these two functions, they're colorama's
    just_fix_windows_console()
    init(autoreset=True)
    
    # Get the bank to print from the user, 'm' is the main bank
    choice = input("Select bank to view (0, 1, m, 2, 3), an (o)ffset or (f) to view all: ")
    
    # Select the bank, raise error if no case matches
    match (choice):
        case '0':
            bank = range(0, 8191)
        case '1':
            bank = range(8192, 16383)
        case '2':
            bank = range(16384, (8192 * 3) - 1)
        case '3':
            bank = range(8192 * 3, 8192 * 4 - 1)
        case 'f' | 'F':
            bank = range(0, 8192 * 4)
        case 'm' | 'M':
            bank = range(0x2598, 0x3523 + 1)
        case 'o' |'O':
            offset = input("Offset: ")
            print(f"Data: {hexdata[offset]}")
            return
        case _:
            raise ValueError
            
    # Select the byte width
    bytes_to_print = int(input("Type in the number of bytes to display: "))
    
    # count is the variable that determines if a newline should be printed 
    # data_string is a placeholder for the bytes' potential meaning before it is printed
    count = 1
    data_string = ""
    print("Printing Hex Data...\n", "-" * 105)
    
    # Start of loop, it loops over every byte in the bank selected
    first = True
    for t in bank:
        # Print the first offset group once 
        if (first):print(("0x" + hex(t)[2:].upper()).ljust(7) + ": ", end="");first = False
        
        # If the current byte is a printable ASCII character, add it to data_string
        if ((hexdata[t] > 31 ) and (hexdata[t]) < 127):
            # If the current character is a period, then print it with colors
            if (chr(hexdata[t]) == "."):
                data_string += Fore.GREEN + Back.YELLOW + (chr(int(hexdata[t]))) + Style.RESET_ALL
            else:
                data_string += chr(int(hexdata[t]))
        
        # If not a printable character, then add a period
        else:
            data_string += "."
            
        # hex_string contains the bytes as they are represented in hexadecimal
        # It is also right-justified for even printing
        hex_string = ("0x" + (hex(hexdata[t]))[2:].upper()).ljust(6, " ")
        
        # If count equals the byte width, then print WITH a newline and reset count, otherwise print without
        # and increment count
        if (count == bytes_to_print):
            print(hex_string, f"# {data_string}\n{('0x' + hex(t)[2:].upper()).ljust(7)}: ", end="")
            data_string = ""
            count = 0
        else:
            print(hex_string, end="")
        count += 1
    print("\n\r", "-" * 105)