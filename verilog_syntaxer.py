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
        self.cur_submodule = None
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
                              "MODULE_CONTENT" : self.__handler_branch,
                              "BLK_PORT_EXP" : self.__handler_blk_port_exp,
                              "BLK_SIG_EXP" : self.__handler_branch,
                              "SUBMODULE" : self.__handler_submodule,
                              "SUBMODULE_INSTANCE" : self.__handler_branch,
                              "SUBMODULE_NAME" : self.__handler_submodule_name,
                              "SUBMODULE_PARAM" : self.__handler_branch,
                              "SUBMODULE_PARAM_LIST" : self.__handler_submodule_param_list,
                              "SUBMODULE_PORT" : self.__handler_branch,
                              "SUBMODULE_PORT_LIST" : self.__handler_submodule_port_list}


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
                (cur_signal_width, _) = self.__handler_width(root.node_left.node_right)

        cur_name = root.node_right.node_left.node_text

        if root.node_right.node_right != None:
            (cur_array_width, _) = self.__handler_width(root.node_right.node_right)

        cur_signal_node = verilog_class.VSignal(cur_name, cur_net_type,
                                                cur_signal_width, cur_array_width)
        self.cur_module.add_signal(signal_type, cur_signal_node)

    @staticmethod
    def __handler_width(root):
        """ Handle the width node """
        if root.node_text == "WIDTH":
            cur_width = abs(int(root.node_right.node_text) - int(root.node_left.node_text))
            cur_text = "[" + root.node_left.node_text + ":" + root.node_right.node_text + "]"
        elif root.node_text == "WIDTH+":
            cur_width = root.node_right.node_text
            cur_text = "[" + root.node_left.node_text + "+:" + root.node_right.node_text + "]"
        else:
            print("ERROR!! Unexpect Width Node")
            quit()

        return (cur_width, cur_text)

    def __handler_blk_port_exp(self, root):
        cur_signal_type = root.node_left.node_text
        self.__handler_signal_exp(root.node_right, cur_signal_type)

    def __handler_submodule(self, root):
        """ Handle the submodule node """
        self.cur_submodule = verilog_class.VSubmodule(root.node_left.node_text)
        self.cur_module.add_submodule(self.cur_submodule)
        self.__handler_branch(root.node_right)

    def __handler_submodule_name(self, root):
        """ Handle the submodule name node """
        self.cur_submodule.update_instance_name(root.node_right.node_text)
        if root.node_left != None:
            self.__handler_branch(root.node_left)

    def __handler_submodule_param_list(self, root):
        """ Handle the submodule param list node """
        connect_add_func = self.cur_submodule.add_param
        self.__handler_connect(root.node_left, connect_add_func)
        if root.node_right != None:
            self.__handler_submodule_param_list(root.node_right)

    def __handler_connect(self, root, connect_add_func):
        connect_name = root.node_left.node_text
        if root.node_right != None:
            connect_vector = self.__handler_vector(root.node_right)
        else:
            connect_vector = ""
        cur_connect = verilog_class.VConnect(connect_name, connect_vector)
        connect_add_func(cur_connect)

    def __handler_vector(self, root):
        if root.node_left != None:
            if root.node_left.node_text == "VECTOR":
                cur_text = "(" + self.__handler_vector(root.node_left) + ")"
            elif root.node_left.node_text == "COLLECT":
                cur_text = "{" + self.__handler_collect(root.node_left) + "}"
            elif root.node_left.node_text == "SIGNAL_IDENTIFIER":
                cur_text = root.node_left.node_left.node_text
                if root.node_left.node_right != None:
                    (_, cur_width_text) = self.__handler_width(root.node_left.node_right)
                    cur_text = cur_text + cur_width_text
            else:
                cur_text = root.node_left.node_text
            cur_text = cur_text + self.__handler_vector_remain(root.node_right)
        else:
            cur_text = ""

        return cur_text

    def __handler_vector_remain(self, root):
        cur_text = ""
        if root.node_left != None:
            cur_text = cur_text + root.node_left.node_text

        if root.node_right != None:
            cur_text = cur_text + self.__handler_vector(root.node_right)
        return cur_text

    def __handler_collect(self, root):
        if root.node_left.node_text == "VECTOR":
            cur_text = self.__handler_vector(root.node_left)
            if root.node_right != None:
                cur_text = cur_text + "," + self.__handler_vector(root.node_right)
        else:
            cur_text = root.node_left.node_text
            cur_text = cur_text + "{" + self.__handler_collect(root.node_right) + "}"

        return cur_text

    def __handler_submodule_port_list(self, root):
        """ Handle the submodule port list node """
        connect_add_func = self.cur_submodule.add_connect
        self.__handler_connect(root.node_left, connect_add_func)
        if root.node_right != None:
            self.__handler_submodule_port_list(root.node_right)
       