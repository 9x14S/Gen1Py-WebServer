if __name__ == "__main__":
    print("This file isn't executable.")
    exit(1)
    
import ctypes
import os

library = ctypes.CDLL(os.path.join("CTools", "savetools.so"))

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
    

def checksum(file) -> int:
    """ Calculates the checksum of the given file. """
    return C_checksum(file)

    
def edit_hex(file, offset=None, value=None):
    if (offset is None):
        offset = int(input("Offset (hex): "), base=16)
    if (value is None):
        value = int(input("Value (hex): "), base=16)
    C_edit_offset(file, offset, value)
    return