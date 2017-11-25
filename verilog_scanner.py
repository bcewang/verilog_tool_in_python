#!/usr/bin/env python
import os
import string
import sys

## Function usage()
def usage():
    print("\nERROR!!")
    print("Usage: verilog_scanner.py [verilog_file]")
    print("Example: verilog_scanner.py usb.v\n")
    quit()

## Function open_file()
def open_file_in_list(verilog_file_path):
    try:
        file = open(verilog_file_path, "r")
        file_text = file.readlines()
        file.close()
        return file_text
    except:
        print ("ERROR!! Unable to open file: ", verilog_file_path)
        quit()


###########################
## Main Start
###########################

## Get the target verilog file
if len(sys.argv) != 2:
    usage()

target_file_path = sys.argv[1]
file_text = open_file_in_list(target_file_path)
for line in file_text:
    print (line)

