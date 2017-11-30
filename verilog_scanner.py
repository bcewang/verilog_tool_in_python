"""
    verilog_scanner.py
    A scanner to handler verilog
"""
#!/usr/bin/env python
import sys
import token_type

## Function usage()
def usage():
    """ This function shows how to use this script """
    print("\nERROR!!")
    print("Usage: verilog_scanner.py [verilog_file]")
    print("Example: verilog_scanner.py usb.v\n")
    quit()

## Function open_file()
def open_file_in_list(verilog_file_path):
    """ This function open a file and return a clean list with each line """
    try:
        with open(verilog_file_path, "r") as file:
            file_text = file.readlines()
            clean_text = []
            for file_line in file_text:
                clean_text.append(str.strip(str(file_line)))
            file.close()
            return clean_text
    except IOError:
        print("ERROR!! Unable to open file: ", verilog_file_path)
        quit()


###########################
## Main Start
###########################

## Get the target verilog file
if len(sys.argv) != 2:
    usage()

TOKEN_DICT = token_type.TokenTypeDict()
for line in open_file_in_list(sys.argv[1]):
    for expression in str.split(line):
        print(expression)
        for char in list(expression):
            token_type_num = TOKEN_DICT.get_symbol_type(char)
            if token_type_num != 999:
                print("Current char ", char, " is ", TOKEN_DICT.get_token_string(token_type_num))
