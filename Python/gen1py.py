# import json
from sys import argv
from colorama import *
import ctypes

library = ctypes.CDLL(".\\CTools\\savetools.so")

C_checksum = library.checksum
C_checksum.argtypes = [ctypes.c_void_p] # Need to change the first argument to FILE *
C_checksum.restype = ctypes.c_int

C_edit_offset = library.edit_offset
C_edit_offset.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char] # Need to change the first argument to FILE *
C_edit_offset.restype = ctypes.c_int

C_open_file = library.open_file
C_open_file.argtypes = [ctypes.c_char_p]


def print_help() -> None:
    print("Usage: python main.py (COMMAND) [FLAG/S]. \n \
       Commands:           help - to print this screen. \n\
                            print - to print the save data. \n\
                            edit - to edit the save data. \n\
                            checksum - to print the computed and extracted checksums. \n\n\
                            All flags marked with '*' aren't implemented yet.\n\
        Flags (WIP):        *-h/--help - override all other flags and print this screen. \n\n\
              print:         The flags -f, -b and -o are exclusive. Only one may be used\n\
                            *-f/--full - to print or export all the data.\n\
                            *-F/--no-format - to print or export the data as-is, \n\
                                    without any formatting (default: hex).\n\
                            *-b/--bank (bank) - to print or export the selected bank.\n\
                                    (bank) can be a number between 0 and 3 or (m)ain.\n\
                            *-o/--offset (offset) - to print the hex value at that offset.\n\
                                    (offset) is a number between 0x0 and 0x7FFF. The number can also be decimal.\n\
                            *-e/--export [filename] - to export the data to a file. \n\
                                    If the file name is omitted, default to the name of the source file.\n\
                            *-H/--hex - to format the data to hex.\n\
                            *-d/--decimal -to format the data to decimal. \n\
                            *-v/--verbose - to verbosely print every action. \n\
                                ")
    return

# Function to edit the memory addresses
def edit_hex(hexdata, offset, val:bytes):
    
    # Open both files, the source and the output file
    # ''.join([argv[1].split(sep=".")[0], "(modified).sav"]
    with open(file='red-output.sav', mode="wb") as saveoutput:
        
        # Exception handling for any incorrect values
        try:
            # Save the previous value for later printing. Then replace the offset with the value
            prev_val = hexdata[offset]
            hexdata[offset] = val
            print(f"Edition done at offset {hex(offset)}, with '{prev_val}' replaced with '{hexdata[offset]}'.")
            saveoutput.write(hexdata)
            return hexdata
        
        # If an exception happens, then exit
        except Exception as e:
            print(f"edit_hex_E; {e}")
            print("Exiting...")
            exit(code=1)

def checksum(data=None, edit=False): 
    '''The checksum is calculated as follows:
    Initialize the checksum byte to 0.
    Binary sum the values in each memory address from 0x2598 to 0x3522 exclusive, ignoring any carryover.
    Invert the result.

    Then the checksum result is inserted at offset 0x3523 to be compared while running.'''
    
    # Invoke and store the computed checksum from a function in C
    computed = C_checksum(argv[1].encode("ascii"))
    if (data is None):
        return computed
    if (edit):
        pass
    return data
    
# Function to open the save file and return it as a bytearray object
def open_file() -> bytearray:
    with open(file=argv[1], mode="rb") as f:
        hexdata = bytearray(f.read())
    return hexdata

# Function to print the selected bank of data to the screen
def print_hexdata(hexdata:bytearray) -> None:
    
    # Ignore these two functions, they're colorama's
    just_fix_windows_console()
    init(autoreset=True)
    
    # Get the bank to print from the user, 'm' is the main bank
    choice: str = input("Select bank to view (0, 1, 2, 3), (m)ain, an (o)ffset or (a)ll: ")
    
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
        case 'a' | 'A':
            bank = range(0, 8192 * 4)
        case 'm' | 'M' | "":
            bank = range(0x2598, 0x3523 + 1)
        case 'o' |'O':
            offset = input("Offset: ")
            if ('x' in offset):
                offset = int(offset, base=16)
            else:
                offset = int(offset)
            print(f"Data: {hexdata[offset]}")
            return
        case _:
            raise ValueError
            
    # Select the byte width
    bytes_to_print = input("Type in the number of bytes to display: ")
    if (bytes_to_print == ""):
        bytes_to_print = 12
    else:
        bytes_to_print = int(bytes_to_print)
    
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
                    
        # TO-DO: Add option to print as ASCII or based on the game's character encoding
        if ((hexdata[t] > 0x7F ) and (hexdata[t]) < 0x9A):
            data_string += Fore.GREEN + Back.YELLOW + (chr(int(hexdata[t]) - 63)) + Style.RESET_ALL
            
        elif ((hexdata[t] > 0x9F ) and (hexdata[t]) < 0xBA):
            data_string += Fore.GREEN + Back.YELLOW + (chr(int(hexdata[t]) - 63)) + Style.RESET_ALL
        
        elif (hexdata[t] == 0xE8):
            data_string += Fore.GREEN + Back.YELLOW + (chr(46)) + Style.RESET_ALL
            
        
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
    
if __name__ == "__main__":
    print("Oops, you're trying to run the module as the program. \nPlease run main.py instead.")
    exit(code=1)