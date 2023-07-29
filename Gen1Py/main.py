from gen1py import *

def main() -> int: 
    # If no arguments are provided, throw an error
    assert (len(argv) >= 3), "A filename (only one) is required and a command (print/edit/help). "
    hexdata: bytearray = open_file()
    
    # Match the argument commands 
    match (argv[2].lower()):
        case "print":
            print_hexdata(hexdata)
            print(Fore.YELLOW + "Done.")
            return 0
        case "edit":
            for i in range(0, 7):
                hexdata = edit_hex(hexdata=hexdata, offset=0x2598 + i, val=0x81)
            print(Fore.YELLOW + "Done.")
            checksum(data=hexdata, edit=True)
            return 0
        case "checksum":
            checksum(hexdata, edit=False)
            return 0
        case "help":
            print_help()
            return 0
        case _:
            raise ValueError

if __name__ == "__main__":
    main()
