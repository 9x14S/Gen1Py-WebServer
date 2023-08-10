from wrapper import *
from printhex import *

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
                check_value = int(checksum(file))
                print(f"(From Python): Returned checksum: 0x{hex(check_value)[2:].upper()}")
                close_file(file)
                return 0
            case "edithex":
                file = open_file(argv[1])
                edit_hex(file)
                return close_file(file)
            case "print":
                if (len(argv) == 4):
                    bank = argv[3]
                else:
                    bank = '1'
                hex_dump(argv[1], bank)
                return 0
            case _:
                raise ValueError("(From Python): Unknown command.")
    except Exception as Ex:
        if (file != 0):
            close_file(file)
        print(f"Exception: {Ex}")

if __name__ == "__main__":
    main()
