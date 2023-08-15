if __name__ == "__main__":
    print("This file isn't executable.")
    exit(code=30)
from Package.Python.item_dict import ITEM_DICT


class Items():
    """ A class container for game item encoding/decoding """
    
    def translate_items(data: list) -> dict:
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
        
        data = self.__reverse_dict(data)
        items = [total, ]
        
        for key in data:
            if (items[0] > 20): # If the amount of items is greater than the max, add terminator
                items.append(0xFF)
                break
            items.append(data[key])
            items[0] += 1
            
        return items
    
    def __reverse_dict(data: dict) -> dict: 
        """ Reverse the key-value pairs  """
        return {y: x for x, y in data.items()}