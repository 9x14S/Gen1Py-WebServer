if __name__ == "__main__":
    print("This file isn't executable.")
    exit(code=30)
    
from Package.Python.printhex import *


class SaveFile():
    def __init__(self, file: bytes):
        self.savefile: bytes = file
    
    def extract_data(self) -> dict:
        
        data = {'rival': translate(hex_dump(self.savefile, selection='rivalv')),
                'name': translate(hex_dump(self.savefile, selection='namev')),
                'money': hex_to_int(hex_dump(self.savefile, selection='moneyv')),
                'coins': hex_to_int(hex_dump(self.savefile, selection='coinsv')),
                'id': int(''.join(str(x) for x in hex_dump(self.savefile, 'idv')), base=16),
                'badges': get_badges(hex_dump(self.savefile, 'badgesv')),
                'pikachu': int(hex_dump(self.savefile, 'pikachuv')[0]),
                'playerstarter': int(hex_dump(self.savefile, 'playerstarterv')[0]),
                'rivalstarter': int(hex_dump(self.savefile, 'rivalstarterv')[0]),
                'items': parse_items(hex_dump(self.savefile, 'itemsv'))
        }
        return data    
       
    def write_data(self, data: dict):
        save = self.savefile
        save[0x2598:0x2598 + 0xB] = data["name"]
        save[0x25F6:0x25F6 + 0xB] = data["rival"]
        save[0x25F3:0x25F3 + 3] = int_to_hex(data["money"])
        save[0x2850:0x2850 + 3] = int_to_hex(data["coins"])
        save[0x2602] = badges_to_hex(data["badges"])
        save[0x29C1] = data['rivalstarter']
        save[0x29C3] = data['playerstarter'] 
        save[0x271C] = data['pikachu']
        save[0x25C9:0x25C9 + 0x2A] = untranslate_items(data['items'])
       
       
# TODO: All of this below
def int_to_hex(data: str | int):
    pass

def badges_to_hex(data: list):
    pass

def untranslate_items(data: list):
    pass