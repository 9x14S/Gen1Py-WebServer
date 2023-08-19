if __name__ == "__main__":
    print("This file isn't executable.")
    exit(code=30)
    
from colorama import *

import os

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

# Badge values. They are all added up
BADGE_DICT = {"Boulder": 1,
              "Cascade": 2, 
              "Thunder": 4, 
              "Rainbow": 8, 
              "Soul": 16, 
              "Marsh": 32, 
              "Volcano": 64, 
              "Earth": 128,
}

# Data display strings
DATA_NAMES = {"rival": "Rival's Name",
              "name": "Player's Name",
              "id": "Player's ID",
              "pikachu": "Pikachu's Happiness (Yellow)",
              "money": "Current Money",
              "coins": "Current Game Corner Coins",
              "items": "Inventory Items",
              "badges": "Currently Owned Badges"
}

# Data modification tips 
DATA_TIPS =  {"rival": "Up to 10 characters. If more than 7, text might look weird.",
              "name": "Up to 10 characters. If more than 7, text might look weird. Might cause Pikachu to stop following you in Pokémon Yellow.",
              "id": "Up to 65,535.",
              "pikachu": "Up to 255",
              "money": "Up to 999,999",
              "coins": "Up to 9,999",
              "items": "Usage: <ITEM>:<AMOUNT>[, <ITEM>: <AMOUNT>]. Previous items are lost if new ones are added. Max: 20 items. If you insert an item more than once, when editing again it will be summed together into one.",
              "badges": "Check which badges you want."
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
    """ Convert decimal string into binary decimal representation """
    hex_data = []
    counter = 2
    if len(data) > 4:
        counter = 3
    for x in range(counter, 0, -1):
        hex_data.append(int(data[:2], base=16))
        data = data[2:]
    return hex_data


def hex_to_int(data: list, selector=False) -> int: 
    """ Convert binary decimal representation into decimal """
    value = ''.join([hex(byte).removeprefix('0x') for byte in data])
    if selector:
        return value
    return int(value)


def get_badges(data: int) -> list: 
    """ Convert the int value to a list of strings """
    if data == 0:
        return []
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
    # Future TODO:
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
    # Future TODO:
    """ Encode the string back to the game's encoding """
    encoded_name = bytearray()
    for char in data:
        encoded_name.append(ord(char) + 63)
    encoded_name.append(0x50)
    while len(encoded_name) < 11:
        encoded_name.append(0)
    return encoded_name
        

def checksum(file: bytearray) -> int:
    """ Calculate the game's save file checksum."""
    checksum_total = bytearray(1)
    for byte in file[0x2598:0x3523]:
        temp = byte + checksum_total[0]
        if temp > 255:
            checksum_total[0] = temp % 256
        else:
            checksum_total[0] += byte
    checksum_total[0] = checksum_total[0] ^ 0xFF
    return checksum_total
   

def get_id(data: list) -> int:
    """ Translate the extracted data into the player's ID"""
    id = ""
    for each in data:
        id += hex(each).removeprefix("0x")
    return int(id, base=16)

def unget_id(data: str) -> list:
    """ Translate back the modified ID into the game's encoding"""
    if int(data) == 0:
        return [0, 0]
    hex_id = hex(int(data)).removeprefix("0x")
    hex_length = len(hex_id)
    hex_length = 4 - hex_length
    while hex_length != 0:
        hex_id = '0' + hex_id
        hex_length -= 1
    id = [int(hex_id[:2], base=16), int(hex_id[2:4], base=16)]
    return id