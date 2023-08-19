if __name__ == "__main__":
    print("This file isn't executable.")
    exit(code=30)
    
from Package.Python.lib import *
from Package.Python.items import Items


class SaveFile():
    def __init__(self, file: bytearray):
        self.savefile: bytearray = file
        print(len(self.savefile)) # Debug
        whatever = Items()
        
        id_data = hex_dump(self.savefile, selection='id')
        self.total_id = id_data[0] * id_data[1]
        
        self.rival_name = translate_name(hex_dump(self.savefile, selection='rival'))
        self.player_name = translate_name(hex_dump(self.savefile, selection='name'))
        
        self.money = hex_to_int(hex_dump(self.savefile, selection='money'))
        self.coins = hex_to_int(hex_dump(self.savefile, selection='coins'))
        self.pikachu_happiness = int(hex_dump(self.savefile, selection='pikachu')[0])

        self.items = whatever.translate_items(hex_dump(self.savefile, selection='items'))
        self.badges = get_badges(int(hex_dump(self.savefile, selection='badges')[0]))
    
    def extract_data(self) -> dict:
        data = {'name': self.player_name,
                'rival': self.rival_name,
                'money': self.money,
                'coins': self.coins,
                'id': self.total_id,
                'pikachu': self.pikachu_happiness,
                'items': self.items
        }
        print(self.badges) # Debug
        return data, self.badges
       
    def write_data(self, data: dict):
        save = self.savefile
        data = self.__check_data(data)

        print(f"\n\nInserting data: {data} \n\n")
        if "name" not in self.check_list:
            save[0x2598:0x2598 + 0xB] = untranslate_name(data["name"])
        if "rival" not in self.check_list:   
            save[0x25F6:0x25F6 + 0xB] = untranslate_name(data["rival"])
        if "money" not in self.check_list:
            money_baby = int_to_hex(data["money"])
            save[0x25F3:0x25F3 + 3] = money_baby
        if "coins" not in self.check_list:
            save[0x2850:0x2850 + 2] = int_to_hex(data["coins"])
        if "badges" not in self.check_list:   
            save[0x2602] = badges_to_int(data["badges"])
        if "pikachu" not in self.check_list:
            save[0x271C] = int(data['pikachu'])
        if "id" not in self.check_list:
            save[0x2605:0x2605 + 2] = int_to_hex(data["id"])
        if "items" not in self.check_list:
            whatever = Items()
            save[0x25C9:0x25C9 + 0x2A] = whatever.untranslate_items(data['items'])
        return save

    def __check_data(self, data: dict) -> dict:
        print(f"Data before sanitization: {data}") # Debug
        check_list = []
        for entry in data:
            if entry == "badges":
                continue
            if len(data[entry]) == 1:
                data[entry] = data[entry][0]

        name_length = len(data["name"])
        if data["name"] == "" or name_length > 10 or name_length < 1:
            if name_length > 10:
                data["name"] = data["name"][:10]
            elif name_length < 1:
                data["name"] = self.player_name
                check_list.append("name")

        rival_length = len(data["rival"])
        if data["rival"] == "" or rival_length > 10 or rival_length < 1:
            if rival_length > 10:
                data["rival"] = data["rival"][:10]
            elif name_length < 1:
                data["rival"] = self.rival_name
                check_list.append("rival")
        
        if data["money"] == "":
            data["money"] = self.money
            check_list.append("money")
        
        if data["id"] == "":
            data["id"] = self.total_id
            check_list.append("id")

        if data["coins"] == "":
            data["coins"] = self.coins
            check_list.append("coins")

        if data["items"] == "":
            data["items"] = self.items
            check_list.append("items")

        data["badges"].remove("BADGE_PLACEHOLDER")
        if data.get("badges") == "":
            if data["badges"] != self.badges:
                check_list.append("badges")
            else:
                data["badges"] = self.badges

        if data["pikachu"] == "":
            data["pikachu"] = self.pikachu_happiness
            check_list.append("pikachu")

        self.check_list = check_list
        print(f"DATA (after sanitizing): {data}") # Debug
        return data