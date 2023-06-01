import json

'''
class Pokemon():
    def __init__(self):
        try:
            with open("pkmn.json", "r") as p:
                data = p.read()
        except Exception:
            print("An error ocurred while importing Pokemon data. ")
            exit(1)
'''

def write_data() -> int:
    with open("red.sav", "rb") as s, open("output.sav", "wb") as o:
        hexdata = bytearray(s.read())
        offset = int(input("Offset: "))
        hexdata[offset] = int(input("Value: "))
        checksum(hexdata)
        o.write(hexdata)
        print("Done.")
    return 0

# Function to compute the checksum needed so that the save doesn't appear corrupted in the game
def checksum(data): 
    # Initilize the checksum variable to 255, then subtract from each each value from the range
    total_checksum = 255
    for i in data[9624:13602+1]:
        total_checksum -= i
    # Then inject it back to its place
    if (total_checksum < 0):
        total_checksum = 0
    data[13603] = total_checksum
    
write_data()