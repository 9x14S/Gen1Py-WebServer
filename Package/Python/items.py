if __name__ == "__main__":
    print("This file isn't executable.")
    exit(code=30)
from Package.Python.item_dict import ITEM_DICT


class Items():
    """ A class container for game item encoding/decoding """
    
    def translate_items(self, data: list) -> dict:
        """ Convert from the in-game representation to a dictionary """
        if data[0] == 0: 
            return {}
        items = {}
        count = 1
        while count <= data[0]:
            key = ITEM_DICT[data[count]]
            if key in items:
                items[key] += data[count + 1]
            else:
                items[key] = data[count + 1]
            count += 2
        return items
    
    def untranslate_items(self, data: str) -> list:
        """ Convert a dictionary of item names and amounts to the in-game representation """
        
        # Get each item name and amount grouped together in a dictionary
        split_data = data.split(',')
        split_data = map(str.strip, split_data)
        container = []
        for dict_entry in split_data:
            data = {}
            split_entry = dict_entry.split(':')
            data[split_entry[0]] = int(split_entry[1])
            container.append(data)
            
        if len(data) == 2 or len(data) == 0:
            empty_items = [0, 0xFF] + [0 for _ in range(40)]
            return empty_items
        
        
        # Invert the keys and values
        REVERSE_DICT = self.__reverse_dict(ITEM_DICT)
        # Start the item counter
        items = [0, ]
        
        # Add to the items list
        # TODO: add checker for non found items
        for entry in container:
            if (items[0] >= 20): # If the amount of items is greater than the max, add terminator
                items.append(0xFF)
                break
            key = [x for x in entry.keys()][0]
            found = REVERSE_DICT.get(key.strip(' '), None)
            if found is None:
                continue
            else:
                items.append(found)
                items.append(entry[key])
                items[0] += 1
        else:
            items.append(0xFF)
            while len(items) < (20 * 2 + 2):
                items.append(0)
        return items
    
    def __reverse_dict(self, data: dict) -> dict: 
        """ Reverse the key-value pairs. """
        return {y: x for x, y in data.items()}