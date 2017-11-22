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
def open_file(verilog_file_path):
    try:
        file = open(verilog_file_path, "r")
        return file
    except:
        print ("ERROR!! Unable to open file: ", verilog_file_path)
        quit()


## Function close_file()
def close_file(target_file):
    try:
        target_file.close()
    except:
        print ("ERROR!! Unable to close file")
        quit()


###########################
## Main Start
###########################

## Get the target verilog file
if len(sys.argv) != 2:
    usage()

target_file_path = sys.argv[1]
target_file = open_file(target_file_path)
file_text = target_file.readlines()
for line in file_text:
    print (line)

