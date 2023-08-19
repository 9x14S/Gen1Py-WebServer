if __name__ == "__main__":
    print("This file isn't executable.")
    exit(code=30)
from Package.Python.item_dict import ITEM_DICT


class Items():
    """ A class container for game item encoding/decoding """
    
    def translate_items(self, data: list) -> dict:
        """ Convert from the in-game representation to a dictionary """
        if data is None or data[0] == 0: 
            return {None: None}
        items = {}
        count = 1
        while count <= data[0]:
            items[ITEM_DICT[data[count]]] = data[count + 1]
            count += 2
        return items
    
    def untranslate_items(self, data: dict) -> list:
        """ Convert a dictionary of item names and amounts to the in-game representation """
        backup = data
        print(f"Data: {data}, type: {type(data)}") # Debug
        data = {x.split(':')[0].strip(): int(x.split(':')[1].strip()) for x in [z for z in data.split(',')]}
        total = len(data) 
        print(f"Item data: {data}") # Debug
        if total == 0 or data is None: # Return empty list if no items 
            empty_items = [0, 0xFF] + [0 for _ in range(40)]
            print(f"Empty items: {empty_items}")
            return empty_items
        
        REVERSE_DICT = self.__reverse_dict(ITEM_DICT)
        items = [0, ]
        
        for key in data:
            if (items[0] >= 20): # If the amount of items is greater than the max, add terminator
                items.append(0xFF)
                break
            items.append(REVERSE_DICT[key])
            items.append(data[key])
            items[0] += 1
        else:
            items.append(0xFF)
            while len(items) < (20 * 2 + 2):
                items.append(0)
            
        print(f"Encoded items: {items}") # Debug
        return items
    
    def __reverse_dict(self, data: dict) -> dict: 
        """ Reverse the key-value pairs  """
        return {y: x for x, y in data.items()}