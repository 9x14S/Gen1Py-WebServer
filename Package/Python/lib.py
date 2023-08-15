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

BADGE_DICT = {"Boulder": 128,
              "Cascade": 64, 
              "Thunder": 32, 
              "Rainbow": 16, 
              "Soul": 8, 
              "Marsh": 4, 
              "Volcano": 2, 
              "Earth": 1
}

def hex_dump(opensave: bytes, selection: str) -> bytes:
    """ Returns the a bytes object containing the selected information. 
    """

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
    
    holder = [opensave[x] for x in bank]
    return holder


def int_to_hex(data: str) -> list: 
    """ Convert decimal into binary decimal representation """
    return [int(x, base=16) for x in data[::2]]


def hex_to_int(data: list, selector=False) -> int: 
    """ Convert binary decimal representation into decimal """
    value = ''.join([hex(byte).removeprefix('0x') for byte in data])
    if selector:
        print(value)
        return value
    return int(value)


def get_badges(data: int) -> list: 
    """ Convert the int value to a list of strings """
    divisor = 128
    
    return_badges = []
    for badge in BADGE_DICT:
        result = data // divisor
        if result:
            return_badges.append(badge)
            data -= divisor
            divisor //= 2
        
    return return_badges
      
def badges_to_int(data: list) -> int: 
    """ Convert back the names of badges to the int value """
    return sum([BADGE_DICT[x] for x in data])

def translate_name(data: list): 
    """ Convert name to ASCII
    Still needs some work to actually encode all characters correctly  """
    output = ''
    for char in data:
        if (char == 80 or char == 0):
            break
        if ((char > 0x7F ) and (char) < 0x9A) or \
            ((char > 0x9F ) and (char) < 0xBA):
            output = ''.join([output, chr(char - 63)])
    return output

def untranslate_name(data: str) -> list: 
    """ Encode the string back to the game's encoding """
    if len(data) > 10:
        data = data[:11]
    return [ord(x) + 63 for x in data].append(0x50)
        
def checksum(save: list) -> int:
    return sum(save[0x2598:0x3522]) % 255

def upload_file_name(name: str) -> str:
    return name.split(".")[0] + "EDITED" + ".sav"