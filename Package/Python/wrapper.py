if __name__ == "__main__":
    print("This file isn't executable.")
    exit(code=30)
    
from Package.Python.lib import *
from Package.Python.items import Items


class SaveFile():
    def __init__(self, file: bytearray):
        self.savefile: bytearray = bytearray(file)
    
    def extract_data(self) -> dict:
        
        data = {'rival': translate_name(hex_dump(self.savefile, selection='rival')),
                'name': translate_name(hex_dump(self.savefile, selection='name')),
                'money': hex_to_int(hex_dump(self.savefile, selection='money')),
                'coins': hex_to_int(hex_dump(self.savefile, selection='coins')),
                'badges': get_badges(int(hex_dump(self.savefile, selection='badges')[0])),
                'id': int(''.join(str(x) for x in hex_dump(self.savefile, selection='id')), base=16),
                'pikachu': int(hex_dump(self.savefile, selection='pikachu')[0]),
                'items': Items.translate_items(hex_dump(self.savefile, selection='items'))
        }
        return data
       
    def write_data(self, data: dict):
        save = self.savefile
        save[0x2598:0x2598 + 0xB] = untranslate_name(data["name"])
        save[0x25F6:0x25F6 + 0xB] = untranslate_name(data["rival"])
        save[0x25F3:0x25F3 + 3] = int_to_hex(data["money"])
        save[0x2850:0x2850 + 3] = int_to_hex(data["coins"])
        save[0x2602] = badges_to_int(data["badges"])
        save[0x271C] = data['pikachu']
        save[0x25C9:0x25C9 + 0x2A] = Items.untranslate_items(data['items'])
        save[0x3523] = checksum(save)
        return save
