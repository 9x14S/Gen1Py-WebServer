from wrapper import *

def main() -> int: 
    # If no arguments are provided, throw an error
    assert (len(argv) >= 3), "A single filename is required and a command. "
    assert ('.gb' not in argv[1].lower()), "Oops, you're trying to view or edit the game. "
    # hexdata: bytearray = open_file()
    """ 
    case "edit":
    for i in range(0, 7):
        hexdata = edit_hex(hexdata=hexdata, offset=0x2598 + i, val=0x81)
    hexdata = edit_hex(hexdata=hexdata, offset=0x2598 + 7, val=0x50)
    print(Fore.YELLOW + "Done.")
    return 0 
    """
    
    # Match the argument commands 
    """ 
        case "print":
        print_hexdata(hexdata)
        print(Fore.YELLOW + "Done.")
        return 0 
    """
    
    file = open_file(argv[1])
    try:
        match (argv[2].lower()):
            case "checksum":
                print(f"(From Python): Returned checksum: {checksum(file)}")
                return 0
            case "edithex":
                offset = int(input("Offset (hex): "), base=16)
                value = int(input("Value: "), base=16)
                return C_edit_offset(argv[1].encode("ascii"), offset, value)
                """ 
            case "help":
            print_help()
            return 0 """
            case _:
                raise ValueError
    except Exception:
        close_file(file)
        print("Error!")

if __name__ == "__main__":
    main()
