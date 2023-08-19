if __name__ == "__main__":
    print("This file isn't executable.")
    exit(code=30)
    
from Package.Python.lib import *
from Package.Python.items import Items


class SaveFile():
    """ A class representing the relevant editable data in the game's save file"""
    
    def __init__(self, file: bytearray):
        self.savefile: bytearray = file # Save the file into the object
        whatever = Items() # Create temporary Items object to manipulate items
        
        # Open the file, read the data and store it in the object
        id_data = hex_dump(self.savefile, selection='id')
        self.total_id = get_id(id_data)
        
        self.rival_name = translate_name(hex_dump(self.savefile, selection='rival'))
        self.player_name = translate_name(hex_dump(self.savefile, selection='name'))
        
        self.money = hex_to_int(hex_dump(self.savefile, selection='money'))
        self.coins = hex_to_int(hex_dump(self.savefile, selection='coins'))
        self.pikachu_happiness = int(hex_dump(self.savefile, selection='pikachu')[0])

        self.items = whatever.translate_items(hex_dump(self.savefile, selection='items'))
        self.badges = get_badges(int(hex_dump(self.savefile, selection='badges')[0]))
    
    def extract_data(self) -> dict:
        
        # Extract the data from the object, make it into a dictionary and send it back
        data = {'name': self.player_name,
                'rival': self.rival_name,
                'money': self.money,
                'coins': self.coins,
                'id': self.total_id,
                'pikachu': self.pikachu_happiness,
                'items': self.items
        }
        return data, self.badges
       
    def write_data(self, data: dict):
        save = self.savefile
        data = self.__check_data(data) # Sanitize the data and run some checks

        # Write the sanitized data to the buffer
        if "name" not in self.check_list:
            save[0x2598:0x2598 + 0xB] = untranslate_name(data["name"])
        if "rival" not in self.check_list:
            save[0x25F6:0x25F6 + 0xB] = untranslate_name(data["rival"])
        if "money" not in self.check_list:
            save[0x25F3:0x25F3 + 3] = int_to_hex(data["money"])
        if "coins" not in self.check_list:
            save[0x2850:0x2850 + 2] = int_to_hex(data["coins"])
        if "badges" not in self.check_list:
            save[0x2602] = badges_to_int(data["badges"])
        if "pikachu" not in self.check_list:
            save[0x271C] = int(data['pikachu'])
        if "id" not in self.check_list:
            save[0x2605:0x2605 + 2] = unget_id(data["id"])
        if "items" not in self.check_list:
            data["items"] = data["items"].strip(', ')
            whatever = Items()
            save[0x25C9:0x25C9 + 0x2A] = whatever.untranslate_items(data['items'])
        return save

    def __check_data(self, data: dict) -> dict:
        # This function checks for wrong or empty data and fixes it
        
        self.check_list = []
        # Get the data out of lists of length 1 unless it is the badges list
        for entry in data:
            if entry == "badges":
                continue
            if len(data[entry]) == 1:
                data[entry] = data[entry][0]

        # Check the provided name is not empty or too long
        name_length = len(data["name"])
        if data["name"] == "" or name_length > 10:
            if name_length > 10:
                # If too long, truncate it
                data["name"] = data["name"][:10]
            else:
                # If empty, use the previous name
                data["name"] = self.player_name
                self.check_list.append("name")

        # Check the provided name is not empty or too long
        rival_length = len(data["rival"])
        if data["rival"] == "" or rival_length > 10 or rival_length < 1:
            if rival_length > 10:
                # If too long, truncate it
                data["rival"] = data["rival"][:10]
            else:
                # If empty, use previous name
                data["rival"] = self.rival_name
                self.check_list.append("rival")
        
        # Check that an amount of money has been provided or that it is not 
        # greater than 999,999
        money_length = len(data["money"])
        if data["money"] == "":
            data["money"] = self.money
            self.check_list.append("money")
        elif int(data["money"]) > 999999:
            data["money"] = "999999"
        elif int(data["money"]) == 0:
            data["money"] = "000000"
        elif money_length < 6:
            data["money"] = data["money"].zfill(6)
        
        # Check that the id falls between the boundaries
        id_length = len(data["id"])
        if data["id"] == "":
            data["id"] = self.total_id
            self.check_list.append("id")
        elif int(data["id"]) > 256 * 256 - 1:
            data["id"] = "65535"
        elif int(data["id"]) == 0:
            data["id"] = "0000"
        elif id_length < 5:
            data["id"] = data["id"].zfill(5)

        # The same as for money
        coins_length = len(data["coins"])
        if data["coins"] == "":
            data["coins"] = self.coins
            self.check_list.append("coins")
        elif int(data["coins"]) == 0:
            data["coins"] = "0000"
        elif int(data["coins"]) > 9999:
            data["coins"] = "9999"
        elif coins_length < 4:
            data["coins"] = data["coins"].zfill(4)
            
        # If no items provided, keep previous
        if data["items"] == "":
            data["items"] = self.items
            self.check_list.append("items")

        # Remove the placeholder that lets the form send even if empty
        # The badge converter will output 0 if the list is empty
        data["badges"].remove("BADGE_PLACEHOLDER")

        if data["pikachu"] == "":
            data["pikachu"] = self.pikachu_happiness
            self.check_list.append("pikachu")
        elif int(data["pikachu"]) > 255:
            data["pikachu"] = "255"

        return data