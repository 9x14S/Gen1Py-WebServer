if __name__ == "__main__":
    print("This file isn't executable.")
    exit(code=30)
    
from colorama import *

BANK0 = range(0x0, 0x2000) # First bank, with hall of fame data
BANK1 = range(0x2000, 0x4000) # Second bank, main bank
BANK2 = range(0x4000, 0x6000) # Third, PC boxes 1-6
BANK3 = range(0x6000, 0x8000) # Fourth, PC boxes 7-12

MAIN = range(0x2598, 0x3523 + 1) # The main data, where the player's data is stored
PLAYERNAME = range(0x2598, 0x2598 + 0xB) # Player's name
RIVALNAME = range(0x25F6, 0x25F6 + 0xB) # Rival's name
ID = range(0x2605, 0x2605 + 2) # Player's trainer ID
MONEY = range(0x25F3, 0x25F3 + 3) # Player's amount of money

BADGES = [0x2602] # Won badges
COINS = range(0x2850, 0x2850 + 2) # Amount of slot coins 
PLAYERSTARTER = [0x29C3] # Player's starter Pokémon
RIVALSTARTER = [0x29C1] # Rival's starter Pokémon
PIKACHU =  [0x271C] # Pikachu's friendship level (Only PKMN Yellow)
ITEMS = range(0x25C9, 0x25C9 + 0x2A) # Items in inventory


def hex_dump(opensave: bytes, selection: str):
    """ Prints a hex dump of all the relevant data in the file. 
        It is a rough copy-paste so some optimizations and fixes are needed. 
        
        filename is the name of the file to be opened.
        selection is the selected bank, offset or group of offsets.
            Adding 'p' to the end prints the selection.
            Adding 'v' returns the value.
            If using both 'p' and 'v', 'p' precedes 'v'. 
        """
        
    just_fix_windows_console() # For windows 

    count = 1

    return_value = False # Return the value printed?
    bytes_to_print = 12 # Byte width for each line, this should be modifiable
    
    if (selection[-1].lower() == 'p'):
        should_print = True # Print or just return the value? 
        selection = selection[0:-1]
        data_string = "" # Buffer to hold the formatted line before printing
    else:
        should_print = False
        
    if (selection[-1].lower() == 'v'):
        selection = selection[0:-1]
        return_value = True
        
    match selection:
        case '0':
            bank = BANK0
        case '1':
            bank = BANK1
        case '2':
            bank = BANK2 
        case '3':
            bank = BANK3
        case 'm' | 'M':
            bank = MAIN
        case 'name':
            bank = PLAYERNAME 
        case 'rival':
            bank = RIVALNAME
        case 'money':
            bank = MONEY
        case 'badges': 
            bank = BADGES
        case 'coins': 
            bank = COINS
        case 'rivalstarter':
            bank = RIVALSTARTER
        case 'playerstarter':
            bank = PLAYERSTARTER
        case 'pikachu':
            bank = PIKACHU
        case 'id':
            bank = ID
        case 'items':
            bank = ITEMS
        case _:
            raise ValueError(f"Unknown bank '{selection}'.")
    
    first = True # Temporary value 
    return_string = []
    
    if (should_print): print("\n\r", "-" * 105)
    
    for byte in bank:
        
        # Print the first offset group once 
        if (first and should_print):
            print(''.join(["0x", hex(byte)[2:].upper()]).ljust(7) + ": ", end="")
            first = False
            
            
        if (return_value):
            return_string.append(opensave[byte])
                    
        # TO-DO: Add option to print as ASCII or based on the game's character encoding
        
        # Add the current character
        if  (((opensave[byte] > 0x7F ) and (opensave[byte]) < 0x9A) or \
            ((opensave[byte] > 0x9F ) and (opensave[byte]) < 0xBA)) and should_print:
            data_string = ''.join([data_string, Fore.GREEN, Back.YELLOW, 
                                    chr(int(opensave[byte]) - 63), 
                                    Style.RESET_ALL]
            )
            
        # If literally a period, add color to it
        elif (opensave[byte] == 0xE8) and should_print:
            data_string += Fore.GREEN + Back.YELLOW + (chr(46)) + Style.RESET_ALL
            
        # If not a printable character, then add a period
        elif (should_print):
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
        
    # Print remaining hex translation
    if (should_print): 
        if (count <= bytes_to_print):
            length = len(hex_string)
            print(f"# {data_string}".rjust(count * (bytes_to_print - length) + 3),  end="")
        print("\n\r", "-" * 105)
        
    if (return_value):
        return return_string
    
    return None

def translate(data_string: list):
    output = ''
    for char in data_string:
        if (char == 80 or char == 0):
            break
        if ((char > 0x7F ) and (char) < 0x9A) or \
            ((char > 0x9F ) and (char) < 0xBA):
            output = ''.join([output, chr(char - 63)])
    return output
                
def hex_to_int(data: list, selector=False):
    value = ''.join([hex(byte).removeprefix('0x') for byte in data])
    if selector:
        print(value)
        return value
    return int(value)

def get_badges(data: list):
    data = data[0]
    divisor = 128
    badges = ["Boulder", "Cascade", "Thunder", "Rainbow", "Soul", "Marsh", "Volcano", "Earth"]
    
    return_badges = []
    for badge in badges:
        result = data // divisor
        if result:
            return_badges.append(badge)
            data -= divisor
            divisor //= 2
        
    return return_badges
            
def get_pokemon(data: list):
    # TODO: 
    return data[0]
    
def translate_items(data: list):
    # TODO:
    return data