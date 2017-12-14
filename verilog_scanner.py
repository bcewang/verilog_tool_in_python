"""
    verilog_scanner.py
    A scanner to handle verilog
"""
#!/usr/bin/env python
import re
import token_type
import verilog_reader

class VerilogScanner:
    """ A verilog scanner """
    def __init__(self, verilog_text_list):
        self.token_query = token_type.TokenTypeDict()
        self.cur_token = token_type.BasicToken()
        self.reader = verilog_reader.VerilogReader(verilog_text_list)
        self.cur_state = "SCAN_CS_IDLE"
        self.text_buf = ""
        self.line_num = 0
        self.handler_query = {"SCAN_CS_IDLE" : self.__handler_scan_idle,
                              "SCAN_CS_START" : self.__handler_scan_start,
                              "SCAN_CS_IDENTIFIER" : self.__handler_scan_identifier,
                              "SCAN_CS_NUMBER" : self.__handler_scan_number,
                              "SCAN_CS_NUMBER_TYPE" : self.__handler_scan_number_type,
                              "SCAN_CS_NUMBER_POST" : self.__handler_scan_number_post}


    def get_next_token(self):
        """ Accord the header of the current content, return a token """
        self.cur_state = "SCAN_CS_START"
        while self.cur_state != "SCAN_CS_IDLE":
            cur_handler = self.handler_query[self.cur_state]
            cur_handler()

        print("GET TOKEN:", self.cur_token.token_type, self.cur_token.token_text)
        new_token = token_type.BasicToken(
            self.cur_token.token_text, self.cur_token.token_type, self.cur_token.line_number)
        return new_token

    def get_line_num(self):
        """ return the current line number """
        return self.line_num

    def __handler_scan_idle(self):
        """ The state handler should not be called """
        print("ERROR!! The handler of IDLE should not be called in state:\n", self.cur_state)
        quit()


    def __handler_scan_start(self):
        """ Get a next char and decide jumping to which state """
        (line, char) = self.reader.get_next_valid_char()
        if char == -1:
            self.cur_token.token_text = "End of File"
            self.cur_token.token_type = self.token_query.token_dict["TOKEN_EOF"]
            self.cur_token.line_number = self.line_num
            self.line_num = line
            self.cur_state = "SCAN_CS_IDLE"
            return
        while re.match(r"\s", char):
            (line, char) = self.reader.get_next_valid_char()
            if char == -1:
                self.cur_token.token_text = "End of File"
                self.cur_token.token_type = self.token_query.token_dict["TOKEN_EOF"]
                self.cur_token.line_number = self.line_num
                self.line_num = line
                self.cur_state = "SCAN_CS_IDLE"
                return

        if re.match(r"[A-Za-z_]", char):
            self.text_buf = char
            self.cur_state = "SCAN_CS_IDENTIFIER"
        elif re.match(r"[0-9]", char):
            self.text_buf = char
            self.cur_state = "SCAN_CS_NUMBER"
        else:
            self.cur_token.token_text = char
            self.cur_token.token_type = self.token_query.get_symbol_type(char)
            self.cur_token.line_number = self.line_num
            self.line_num = line
            self.cur_state = "SCAN_CS_IDLE"

        return


    def __handler_scan_identifier(self):
        """ Get a next char and see if the identifier is completed """
        (line, char) = self.reader.get_next_valid_char()

        if char == -1:
            # End of file
            self.cur_token.token_text = self.text_buf
            self.cur_token.token_type = self.token_query.get_symbol_type(self.text_buf)
            if self.cur_token.token_type == -1:
                self.cur_token.token_type = self.token_query.token_dict["TOKEN_VARIABLE"]
            self.cur_token.line_number = self.line_num
            self.line_num = line
            self.cur_state = "SCAN_CS_IDLE"
        elif re.match(r"[0-9A-Za-z_]", char):
            self.text_buf = self.text_buf + char
            self.cur_state = "SCAN_CS_IDENTIFIER"
        else:
            if re.match(r"\S", char):
                self.reader.retract(1)
            self.cur_token.token_text = self.text_buf
            self.cur_token.token_type = self.token_query.get_symbol_type(self.text_buf)
            if self.cur_token.token_type == -1:
                self.cur_token.token_type = self.token_query.token_dict["TOKEN_VARIABLE"]
            self.cur_token.line_number = self.line_num
            self.line_num = line
            self.cur_state = "SCAN_CS_IDLE"

        return

    def __handler_scan_number(self):
        """ Get a next char and see if the number is completed """
        (line, char) = self.reader.get_next_valid_char()

        if re.match(r"[0-9]", char):
            self.text_buf = self.text_buf + char
            self.cur_state = "SCAN_CS_NUMBER"
        elif char == "'":
            self.text_buf = self.text_buf + char
            self.cur_state = "SCAN_CS_NUMBER_TYPE"
        else:
            if re.match(r"\S", char):
                self.reader.retract(1)
            self.cur_token.token_text = self.text_buf
            self.cur_token.token_type = self.token_query.token_dict["TOKEN_NUMBER"]
            self.cur_token.line_number = self.line_num
            self.line_num = line
            self.cur_state = "SCAN_CS_IDLE"

        return


    def __handler_scan_number_type(self):
        """ Get a next char and see if the number type is correct """
        (_, char) = self.reader.get_next_valid_char()

        if re.match(r"[hdob]", char):
            self.text_buf = self.text_buf + char
            self.cur_state = "SCAN_CS_NUMBER_POST"
        else:
            print("ERROR!! A number with a \"'\" should followed the type of number\n")
            print("Now receive a \"", char, "\"\n")
            quit()

        return


    def __handler_scan_number_post(self):
        """ Get a next char and see if the number is completed """
        (line, char) = self.reader.get_next_valid_char()

        if re.match(r"[0-9a-fA-F]", char):
            self.text_buf = self.text_buf + char
            self.cur_state = "SCAN_CS_NUMBER_POST"
        else:
            if re.match(r"\S", char):
                self.reader.retract(1)
            self.cur_token.token_text = self.text_buf
            self.cur_token.token_type = self.token_query.token_dict["TOKEN_NUMBER"]
            self.cur_token.line_number = self.line_num
            self.line_num = line
            self.cur_state = "SCAN_CS_IDLE"

        return
