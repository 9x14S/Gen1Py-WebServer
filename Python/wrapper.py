if __name__ == "__main__":
    print("This file isn't executable.")
    exit(1)
    
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
C_open_file.restype = ctypes.c_void_p

C_close_file = library.close_file
C_close_file.argtypes = [ctypes.c_void_p]
C_close_file.restype = ctypes.c_int


def open_file(filename: str):
    file = C_open_file(filename.encode("ascii"))
    return file


def close_file(file):
     return C_close_file(file)
    

def checksum(file, edit: bool=False) -> int:
    return C_checksum(file)

    
def hex_dump(file, range: int):
    pass
