"""
    verilog_parser.py
    A parser to handle verilog
"""
#!/usr/bin/env python
import sys
import verilog_parser
import common_tool

## Function usage()
def usage():
    """ This function shows how to use this script """
    print("\nERROR!!")
    print("Usage: verilog_scanner.py [verilog_file]")
    print("Example: verilog_scanner.py usb.v\n")
    quit()

###########################
## Main Start
###########################

## Get the target verilog file
if len(sys.argv) != 2:
    usage()

PARSER = verilog_parser.VerilogParser(common_tool.open_file_in_list(sys.argv[1]))

#cur_token = SCANNER.get_next_token()
#while cur_token.token_type != 0:
#    print(cur_token.token_type, cur_token.token_text)
#    if cur_token.token_type == -1:
#        quit()
#    cur_token = SCANNER.get_next_token()
#print(cur_token.token_type, cur_token.token_text)
