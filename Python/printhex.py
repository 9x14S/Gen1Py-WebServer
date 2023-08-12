if __name__ == "__main__":
    print("This file isn't executable.")
    exit(1)
    
from colorama import *

def hex_dump(filename: str, selection: str):
    """ Prints a hex dump of all the relevant data in the file. 
        It is a rough copy-paste so some optimizations and fixes are needed. """
        
    just_fix_windows_console() # For windows 
    
    with open(filename, 'rb') as save:
        opensave = save.read()
        count = 1
        data_string = "" # Buffer to hold the formatted line before printing
        bytes_to_print = 12 # Byte width for each line, this should be modifiable
        return_value = False # Return the value printed?
        if (selection[-1].lower() == 'p'):
            should_print = True # Print or just return the value? 
            selection = selection[0:-1]
        else:
            should_print = False
        match selection:
            case '0':
                bank = range(0x0, 0x2000) # First bank, with hall of fame data
            case '1':
                bank = range(0x2000, 0x4000) # Second bank, main bank
            case '2':
                bank = range(0x4000, 0x6000) # Third, PC boxes 1-6
            case '3':
                bank = range(0x6000, 0x8000) # Fourth, PC boxes 7-12
            case 'm' | 'M':
                bank = range(0x2598, 0x3523 + 1) # The main data, where the player's data is stored
            case 'name':
                bank = range(0x2598, 0x2598 + 11)
                return_value = True
            case 'money':
                bank = range(0x25F3, 0x25F3 + 3)
                return_value = True
            case 'id':
                bank = range(0x2605, 0x2605 + 3)
                return_value = True
            case _:
                raise ValueError(f"Unknown bank '{selection}'.")
        
        first = True # Temporary value 
        return_string = []
        for byte in bank:
            # Print the first offset group once 
            if (first and should_print):
                print(''.join(["0x", hex(byte)[2:].upper()]).ljust(7) + ": ", end="")
                first = False
            if (return_value):
                return_string.append(opensave[byte])
                        
            # TO-DO: Add option to print as ASCII or based on the game's character encoding
            
            # Add the current character
            if ((opensave[byte] > 0x7F ) and (opensave[byte]) < 0x9A) or \
               ((opensave[byte] > 0x9F ) and (opensave[byte]) < 0xBA):
                   
                data_string = ''.join([data_string, Fore.GREEN, Back.YELLOW, 
                                        chr(int(opensave[byte]) - 63), 
                                        Style.RESET_ALL]
                )
                
            # If literally a period, add color to it
            elif (opensave[byte] == 0xE8):
                data_string += Fore.GREEN + Back.YELLOW + (chr(46)) + Style.RESET_ALL
                
            # If not a printable character, then add a period
            else:
                data_string = ''.join([data_string, '.'])
                
            # hex_string contains the bytes as they are represented in hexadecimal
            # It is also right-justified for even printing
            hex_string = ("0x" + (hex(opensave[byte]))[2:].upper()).ljust(6, " ")
            
            # Print values based on byte width
            if (count == bytes_to_print and should_print):
                print(hex_string, f"# {data_string}\n{('0x' + hex(byte)[2:].upper()).ljust(7)}: ", end="")
                data_string = ""
                count = 0
                
            elif (should_print):
                print(hex_string, end="")
                
            count += 1
        if (should_print): print("\n\r", "-" * 105)
        if (return_value):
            return return_string
    return

def translate(data_string: list):
    output = ''
    for char in data_string:
        if (char == 80 or char == 0):
            break
        if ((char > 0x7F ) and (char) < 0x9A) or \
            ((char > 0x9F ) and (char) < 0xBA):
            output = ''.join([output, chr(char - 63)])
    return output
                   