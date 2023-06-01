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

def edit_hex(file:str, edt, val, hex=True):
    with open(file, "rb") as savesource, open("save.sav","wb") as saveoutput:
        try:
            hexdata = bytearray(savesource.read())
            if hex:
                offset = int(edt, base=16)
                hexdata[offset] = int(val.capitalize(), base=16)
            else:
                offset = int(edt)
                hexdata[offset] = int(val)
            saveoutput.write(hexdata)
            return saveoutput
        except Exception as e:print(f"hex_E; {e}")

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

