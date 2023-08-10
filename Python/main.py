from wrapper import *

file = 0

def main() -> int: 
    global file
    # If no arguments are provided, throw an error
    assert (len(argv) >= 3), "A single filename is required and a command. "
    assert ('.gb' not in argv[1].lower()), "Oops, you're trying to view or edit the game. "
   

    try:
        match (argv[2].lower()):
            case "checksum":
                file = open_file(argv[1])
                print(f"(From Python): Returned checksum: 0x{hex(checksum(file))[2:].upper()}")
                return 0
            case "edithex":
                file = open_file(argv[1])
                offset = int(input("Offset (hex): "), base=16)
                value = int(input("Value (hex): "), base=16)
                C_edit_offset(file, offset, value)
                return close_file(file)
            case "print":
                hex_dump(argv[1])
                return 0
            case _:
                raise ValueError("Unknown command.")
    except Exception as Ex:
        if (file != 0):
            close_file(file)
        print(f"Exception: {Ex}")

if __name__ == "__main__":
    main()
