if __name__ == "__main__":
    print("This file isn't executable.")
    exit(code=30)
from Package.Python.item_dict import ITEM_DICT


class Items():
    """ A class container for game item encoding/decoding """
    
    def translate_items(self, data: list) -> dict:
        """ Convert from the in-game representation to a dictionary """
        if data[0] == 0: 
            return {None: None}
        items = {}
        count = 1
        while count <= data[0]:
            items[ITEM_DICT[data[count]]] = data[count + 1]
            count += 2
            print(items)

        return items
    
    def untranslate_items(self, data: dict) -> list:
        """ Convert a dictionary of item names and amounts to the in-game representation """
        total = len(data) 
        if total == 0 or None in data: # Return empty list if no items 
            return [0, 0xFF]
        
        REVERSE_DICT = self.__reverse_dict(ITEM_DICT)
        items = [0, ]
        
        for key in data:
            if (items[0] > 20): # If the amount of items is greater than the max, add terminator
                items.append(0xFF)
                break
            items.append(REVERSE_DICT[key])
            items.append(data[key])
            items[0] += 1
        else:
            items.append(0xFF)
            
        print(items) # Debug
        return items
    
    def __reverse_dict(self, data: dict) -> dict: 
        """ Reverse the key-value pairs  """
        return {y: x for x, y in data.items()}