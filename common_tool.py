"""
    common_tool.py
    Collect gernal purpose functions:
        open_file_in_list([file_path])
"""
import re


## Function remove_comment_in_list()
def remove_comment_in_list(file_content_list):
    """ This function remove the commented partition of the file content in the list """
    multi_line_comment_flag = 0
    new_file_content_list = []

    for line in file_content_list:
        new_line = line
        if multi_line_comment_flag:
            # First, handle multi-line comment
            if re.search(r"\*/", new_line):
                new_line = re.sub(r".*\*/", "", line)
                multi_line_comment_flag = 0
            else:
                new_line = ""
            # Second, clear one-line comment
            if re.search(r"//", new_line):
                new_line = re.sub(r"//.*", "", new_line)
        else:
            # First, clear one-line comment
            if re.search(r"//", new_line):
                new_line = re.sub(r"//.*", "", new_line)
            # Second, handle multi-line comment
            if re.search(r"/\*", new_line):
                multi_line_comment_flag = 1
                new_line = re.sub(r"/\*.*", "", new_line)

        # Final, push new_line if it is not empty
        if new_line != "":
            new_file_content_list.append(new_line)

    return new_file_content_list


## Function open_file_in_list()
def open_file_in_list(verilog_file_path):
    """ This function open a file and return a clean list with each line """
    try:
        with open(verilog_file_path, "r") as file:
            file_text = file.readlines()
            new_file_text = remove_comment_in_list(file_text)
            clean_text = []
            for file_line in new_file_text:
                new_line = str.strip(str(file_line))
                if new_line != "":
                    clean_text.append(new_line)
            file.close()
            return clean_text
    except IOError:
        print("ERROR!! Unable to open file: ", verilog_file_path)
        quit()
