from gen1py import *

def main() -> int: 
    hexdata = open_file()
    print_hexdata(hexdata)
    return 0

if __name__ == "__main__":
    main()