"""
    verilog_reader.py
    A reader to read verilog file and output cur char and next char
"""
class VerilogReader:
    """ A verilog reader """
    def __init__(self, verilog_text_list):
        self.text_list = verilog_text_list
        self.total_line_num = len(verilog_text_list)
        self.cur_line_num = 0
        self.cur_line = self.text_list[self.cur_line_num]
        self.cur_position = 0
        self.cur_boundary = len(self.cur_line)

    def __get_next_char(self):
        """ return a char or -1 if there is no remained char"""
        if self.cur_position >= self.cur_boundary:
            return -1

        next_char = self.cur_line[self.cur_position]
        self.cur_position = self.cur_position + 1
        return next_char


    def retract(self, retract_num=1):
        """ move back the position """
        self.cur_position = self.cur_position - retract_num
        if self.cur_position < 0:
            self.cur_position = 0


    def get_next_valid_char(self):
        """ Get next valid char in the reader """
        char = self.__get_next_char()
        if char == -1:
            self.cur_line_num = self.cur_line_num + 1
            if self.cur_line_num < self.total_line_num:
                self.cur_line = self.text_list[self.cur_line_num]
                self.cur_boundary = len(self.cur_line)
                self.cur_position = 0
                char = '\n'
            else:
                return (self.cur_line_num, -1)

        return (self.cur_line_num, char)
