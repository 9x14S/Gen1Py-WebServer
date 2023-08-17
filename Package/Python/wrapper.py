if __name__ == "__main__":
    print("This file isn't executable.")
    exit(code=30)
    
from Package.Python.lib import *
from Package.Python.items import Items


class SaveFile():
    def __init__(self, file: bytearray):
        self.savefile: bytearray = file
        print(len(self.savefile)) # Debug
    
    def extract_data(self) -> dict:
        whatever = Items()
        data = {'rival': translate_name(hex_dump(self.savefile, selection='rival')),
                'name': translate_name(hex_dump(self.savefile, selection='name')),
                'money': hex_to_int(hex_dump(self.savefile, selection='money')),
                'coins': hex_to_int(hex_dump(self.savefile, selection='coins')),
                'id': int(''.join(str(x) for x in hex_dump(self.savefile, selection='id')), base=16),
                'pikachu': int(hex_dump(self.savefile, selection='pikachu')[0]),
                'items': whatever.translate_items(hex_dump(self.savefile, selection='items'))
        }
        badges = get_badges(int(hex_dump(self.savefile, selection='badges')[0]))
        print(badges) # Debug
        return data, badges
       
    def write_data(self, data: dict):
        save = self.savefile
        data = self.__check_data(data)
        print(data)
        save[0x2598:0x2598 + 0xB] = untranslate_name(data["name"])
        save[0x25F6:0x25F6 + 0xB] = untranslate_name(data["rival"])
        save[0x25F3:0x25F3 + 3] = int_to_hex(data["money"])
        save[0x2850:0x2850 + 2] = int_to_hex(data["coins"])
        save[0x2602] = badges_to_int(data["badges"])
        save[0x271C] = int(data['pikachu'])
        save[0x2605:0x2605 + 2] = int_to_hex(data["id"])
        whatever = Items()
        save[0x25C9:0x25C9 + 0x2A] = whatever.untranslate_items(data['items'])
        return save

    def __check_data(self, data: dict) -> dict:
        
        for entry in data:
            if len(data[entry]) == 1:
                data[entry] = data[entry][0]

        # print(f"DATA (before sanitizing): {data}") # Debug
        name_length = len(data["name"])
        if data["rival"] == "" or name_length > 10 or name_length < 1:
            if name_length > 10:
                data["name"] = data["name"][:11]
            elif name_length < 1:
                data["name"] = translate_name(self.savefile[0x2598:0x2598 + 0xB])

        rival_length = len(data["rival"])
        if data["rival"] == "" or rival_length > 10 or rival_length < 1:
            if rival_length > 10:
                data["rival"] = data["rival"][:11]
            elif name_length < 1:
                data["rival"] = translate_name(self.savefile[0x25F6:0x25F6 + 0xB])
        
        if data["money"] == "":
            data["money"] = "000000"
        
        if data["id"] == "":
            data["id"] = "0000"

        if data["coins"] == "":
            data["coins"] = "0000"
        
        if data["items"] is None:
            whatever = Items()
            data["items"] = whatever.translate_items(self.savefile[0x25C9:0x25C9 + 0x2A])

        if data.get("badges") is None:
            data["badges"] = get_badges(self.savefile[0x2602])

        if data["pikachu"] == "":
            data["pikachu"] = "0"
        print(f"DATA (after sanitizing): {data}") # Debug
        return data