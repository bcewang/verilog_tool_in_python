"""
    verilog_syntaxer.py
    A syntaxer to handle parsing tree
"""
import verilog_parser
import parsing_tree_type
import verilog_class

class VerilogSyntaxer:
    """ A verilog syntaxerer """
    def __init__(self, vfile_name, verilog_text_list):
        self.parser = verilog_parser.VerilogParser(verilog_text_list)
        self.node_query = parsing_tree_type.NodeTypeDict()
        self.cur_file = None
        self.cur_module = None
        self.handler_query = {"VFILE" : self.__handler_branch,
                              "TIMESCALE" : self.__handler_timescale,
                              "DEFINE" : self.__handler_define,
                              "EOF" : self.__handler_eof,
                              "MODULE" : self.__handler_module,
                              "MODULE_BODY" : self.__handler_branch,
                              "MODULE_PORT" : self.__handler_branch,
                              "MODULE_PORT_LIST" : self.__handler_branch,
                              "MODULE_PORT_EXP" : self.__handler_module_port_exp,
                              "SIGNAL_EXP" : self.__handler_signal_exp,
                              "MODULE_CONTENT" : self.__handler_module_content}

        self.__parsing_tree_handler(self.parser.parsing_tree, vfile_name)

    def __parsing_tree_handler(self, parsing_tree, vfile_name):
        if (parsing_tree.node_type == self.node_query.node_dict["NODE_VERILOG_FILE"] and
                parsing_tree.node_left.node_type == self.node_query.node_dict["NODE_VERILOG_FILE"]):
            self.cur_file = verilog_class.VFile(vfile_name)
            self.__handler_branch(parsing_tree.node_left)
        else:
            print("ERROR!! The parsing tree is unexpected")
            quit()

    def __handler_branch(self, root):
        """ Handle the meaningless branch node """
        if root.node_left != None:
            cur_handler = self.handler_query[root.node_left.node_text]
            cur_handler(root.node_left)

        if root.node_right != None:
            cur_handler = self.handler_query[root.node_right.node_text]
            cur_handler(root.node_right)

    def __handler_timescale(self, root):
        """ Handle the timescale node """
        cur_timeunit = (root.node_left.node_left.node_text +
                        root.node_left.node_right.node_text)
        cur_timeprecision = (root.node_right.node_left.node_text +
                             root.node_right.node_right.node_text)
        self.cur_file.timeunit = cur_timeunit
        self.cur_file.timeprecision = cur_timeprecision

    def __handler_define(self, root):
        """ Handle the define node """
        if root.node_right != None:
            self.cur_file.add_define(root.node_left.node_text, root.node_right.node_text)
        else:
            self.cur_file.add_define(root.node_left.node_text, "")

    def __handler_eof(self, root):
        """ Handle the eof node """
        self.cur_file.dump()

    def __handler_module(self, root):
        """ Handle the module node """
        self.cur_module = verilog_class.VModule(root.node_left.node_text)
        self.cur_file.add_module(self.cur_module)
        self.__handler_branch(root.node_right)

    def __handler_module_port_exp(self, root):
        """ Handle the module port exp node """
        if root.node_left != None:
            cur_signal_type = root.node_left.node_text
        else:
            cur_signal_type = "net"

        self.__handler_signal_exp(root.node_right, cur_signal_type)

    def __handler_signal_exp(self, root, signal_type="net"):
        """ Handle the signal exp node """
        cur_net_type = "wire"
        cur_signal_width = 0
        cur_array_width = 0
        if root.node_left != None:
            if root.node_left.node_left != None:
                cur_net_type = root.node_left.node_left.node_text

            if root.node_left.node_right != None:
                cur_signal_width = self.__handler_width(root.node_left.node_right)

        cur_name = root.node_right.node_left.node_text

        if root.node_right.node_right != None:
            cur_array_width = self.__handler_width(root.node_right.node_right)

        cur_signal_node = verilog_class.VSignal(cur_name, cur_net_type,
                                                cur_signal_width, cur_array_width)
        self.cur_module.add_signal(signal_type, cur_signal_node)

    @staticmethod
    def __handler_width(root):
        """ Handle the width node """
        if root.node_text == "WIDTH":
            cur_width = abs(root.node_right.node_text - root.node_left.node_text)
        elif root.node_text == "WIDTH+":
            cur_width = root.node_right.node_text
        else:
            print("ERROR!! Unexpect Width Node")
            quit()

        return cur_width

    def __handler_module_content(self, root):
        """ Handle the eof node """
        pass
