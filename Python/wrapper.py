if __name__ == "__main__":
    print("This file isn't executable.")
    exit(1)
    
from sys import argv
from colorama import *
import ctypes

library = ctypes.CDLL(".\\CTools\\savetools.so")

C_checksum = library.checksum
C_checksum.argtypes = [ctypes.c_void_p]
C_checksum.restype = ctypes.c_int

C_edit_offset = library.edit_offset
C_edit_offset.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char] 
C_edit_offset.restype = ctypes.c_int

C_open_file = library.open_file
C_open_file.argtypes = [ctypes.c_char_p]
C_open_file.restype = ctypes.c_void_p

C_close_file = library.close_file
C_close_file.argtypes = [ctypes.c_void_p]
C_close_file.restype = ctypes.c_int


def open_file(filename: str):
    """ Opens a file as 'rb+' and returns a pointer to it. """
    file = C_open_file(filename.encode("ascii"))
    return file


def close_file(file):
    """ Closes the file pointed at by 'file' """
    return C_close_file(file)
    

def checksum(file, edit: bool=False) -> int:
    """ Calculates the checksum of the given file. """
    return C_checksum(file)

    
def hex_dump(filename: str):
    """ Prints a hex dump of all the relevant data in the file. 
        It is a rough copy-paste so some optimizations and fixes are needed. """
    with open(filename, 'rb') as save:
        opensave = save.read()
        count = 1
        data_string = "" # Buffer to hold the formatted line before printing
        bytes_to_print = 12 # Byte width for each line
        print("Printing Hex Data...\n", "-" * 105)
        
        bank = range(0x2598, 0x3523 + 1) # The main bank, where the player's data is stored
        
        first = True # Temporary value 
        
        for byte in bank:
            # Print the first offset group once 
            if (first):print(("0x" + hex(byte)[2:].upper()).ljust(7) + ": ", end=""); first = False
                        
            # TO-DO: Add option to print as ASCII or based on the game's character encoding
            if ((opensave[byte] > 0x7F ) and (opensave[byte]) < 0x9A):
                data_string += Fore.GREEN + Back.YELLOW + (chr(int(opensave[byte]) - 63)) + Style.RESET_ALL
                
            elif ((opensave[byte] > 0x9F ) and (opensave[byte]) < 0xBA):
                data_string += Fore.GREEN + Back.YELLOW + (chr(int(opensave[byte]) - 63)) + Style.RESET_ALL
            
            elif (opensave[byte] == 0xE8):
                data_string += Fore.GREEN + Back.YELLOW + (chr(46)) + Style.RESET_ALL
                
            
            # If not a printable character, then add a period
            else:
                data_string += "."
                
            # hex_string contains the bytes as they are represented in hexadecimal
            # It is also right-justified for even printing
            hex_string = ("0x" + (hex(opensave[byte]))[2:].upper()).ljust(6, " ")
            
            # If count equals the byte width, then print WITH a newline and reset count, otherwise print without
            # and increment count
            if (count == bytes_to_print):
                print(hex_string, f"# {data_string}\n{('0x' + hex(byte)[2:].upper()).ljust(7)}: ", end="")
                data_string = ""
                count = 0
            else:
                print(hex_string, end="")
            count += 1
        print("\n\r", "-" * 105)