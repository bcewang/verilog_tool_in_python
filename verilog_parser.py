"""
    verilog_parser.py
    A parser to handle verilog
"""
import verilog_scanner
import token_type
import parsing_tree_type

class VerilogParser:
    """ A verilog parser """
    def __init__(self, verilog_text_list):
        self.scanner = verilog_scanner.VerilogScanner(verilog_text_list)
        self.cur_token = self.scanner.get_next_token()
        self.nxt_token = self.scanner.get_next_token()
        self.token_query = token_type.TokenTypeDict()
        self.node_query = parsing_tree_type.NodeTypeDict()
        self.parsing_tree = parsing_tree_type.BasicNode(
            "ROOT", self.node_query.node_dict["NODE_VERILOG_FILE"], None)
        self.parsing_tree.node_left = self.syn_verilog_file(None)
        self.print_parsing_tree(self.parsing_tree)

    def print_parsing_tree(self, root):
        """ Recursive print the text of all nodes """
        if root.node_type != self.node_query.node_dict["NODE_EMPTY"]:
            print(root.node_text, end='')
            if root.node_left != None:
                print("->", end='')
                self.print_parsing_tree(root.node_left)
            if root.node_right != None:
                print("\n-->", end='')
                self.print_parsing_tree(root.node_right)

    def error_unexpect_token(self, source):
        """ Encounter unexpect token, stop parsing """
        print("ERROR!! Unexpect token when", source, self.cur_token.token_type
              , self.cur_token.token_text, self.nxt_token.token_type, self.nxt_token.token_text)
        self.print_parsing_tree(self.parsing_tree)
        quit()

    def consume_cur_token(self, times=1):
        """ Pop the used tokens """
        for _ in range(times):
            self.cur_token = self.nxt_token
            self.nxt_token = self.scanner.get_next_token()

    def syn_verilog_file(self, parent):
        """ VERILOG_FILE node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_EOF"]:
            vfile_node = parsing_tree_type.BasicNode(
                "", self.node_query.node_dict["NODE_EMPTY"], parent)
        else:
            vfile_node = parsing_tree_type.BasicNode(
                "VFILE", self.node_query.node_dict["NODE_VERILOG_FILE"], parent)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_GRAVE"]:
            if self.nxt_token.token_text == "timescale":
                self.consume_cur_token(2)
                vfile_node.node_left = self.syn_timescale(vfile_node)
            elif self.nxt_token.token_text == "define":
                self.consume_cur_token(2)
                vfile_node.node_left = self.syn_define(vfile_node)
            else:
                self.error_unexpect_token("verilog_file1")
        elif self.nxt_token.token_text == "module":
            self.consume_cur_token(1)
            vfile_node.node_left = self.syn_module(vfile_node)
        else:
            #self.error_unexpect_token("verilog_file2")
            module_node = parsing_tree_type.BasicNode()
            return module_node

        vfile_node.node_right = self.syn_verilog_file(vfile_node)
        return vfile_node

    def syn_timescale(self, parent):
        """ BLK_TIMESCALE node handler """
        timescale_node = parsing_tree_type.BasicNode(
            "TIMESCALE", self.node_query.node_dict["NODE_BLK_TIMESCALE"], parent)
        timescale_node.node_left = self.syn_timeunit(timescale_node)
        timescale_node.node_right = self.syn_timeprecision(timescale_node)
        return timescale_node

    def syn_timeunit(self, parent):
        """ BLK_TIMEUNIT node handler """
        timeunit_node = parsing_tree_type.BasicNode(
            "TIMEUNIT", self.node_query.node_dict["NODE_BLK_TIMEUNIT"], parent)
        timeunit_node.node_left = self.syn_number(timeunit_node)
        timeunit_node.node_right = self.syn_keyunit(timeunit_node)
        return timeunit_node

    def syn_number(self, parent):
        """ EXP_NUMBER node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_NUMBER"]:
            number_node = parsing_tree_type.BasicNode(
                self.cur_token.token_text, self.node_query.node_dict["NODE_EXP_NUMBER"], parent)
            self.consume_cur_token(1)
            return number_node
        else:
            self.error_unexpect_token("number")

    def syn_keyunit(self, parent):
        """ EXP_NUMBER node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_KEYUNIT"]:
            keyunit_node = parsing_tree_type.BasicNode(
                self.cur_token.token_text, self.node_query.node_dict["NODE_EXP_KEYUNIT"], parent)
            self.consume_cur_token(1)
            return keyunit_node
        else:
            self.error_unexpect_token("keyunit")


    def syn_timeprecision(self, parent):
        """ BLK_TIMEPRECISION node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_SLASH"]:
            self.consume_cur_token(1)
            timeprecision_node = parsing_tree_type.BasicNode(
                "TIMEPRECISION", self.node_query.node_dict["NODE_BLK_TIMEPRECISION"], parent)
            timeprecision_node.node_left = self.syn_number(timeprecision_node)
            timeprecision_node.node_right = self.syn_keyunit(timeprecision_node)
            return timeprecision_node
        else:
            self.error_unexpect_token("timeprecision")

    def syn_define(self, parent):
        """ BLK_DEFINE node handler """
        define_node = parsing_tree_type.BasicNode(
            "DEFINE", self.node_query.node_dict["NODE_BLK_DEFINE"], parent)
        if self.cur_token.line_number == self.nxt_token.line_number:
            # cur_token.line_number will change when syn_name
            define_node.node_left = self.syn_name(define_node)
            define_node.node_right = self.syn_define_value(define_node)
        else:
            define_node.node_left = self.syn_name(define_node)

        return define_node

    def syn_name(self, parent):
        """ BLK_DEFINE_NAME node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_VARIABLE"]:
            define_name_node = parsing_tree_type.BasicNode(
                self.cur_token.token_text, self.node_query.node_dict["NODE_EXP_NAME"], parent)
            self.consume_cur_token(1)
            return define_name_node
        else:
            self.error_unexpect_token("define_name")

    def syn_define_value(self, parent):
        """ BLK_DEFINE_NAME node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_NUMBER"]:
            define_value_node = parsing_tree_type.BasicNode(
                self.cur_token.token_text, self.node_query.node_dict["NODE_BLK_DEFINE_VALUE"], parent)
            self.consume_cur_token(1)
            return define_value_node
        else:
            self.error_unexpect_token("define_value")

    def syn_module(self, parent):
        """ BLK_MODULE node handler """
        module_node = parsing_tree_type.BasicNode(
            "MODULE", self.node_query.node_dict["NODE_BLK_MODULE"], parent)
        module_node.node_left = self.syn_name(module_node)
        module_node.node_right = self.syn_module_body(module_node)
        return module_node

    def syn_module_body(self, parent):
        """ BLK_MODULE_BODY node handler """
        module_body_node = parsing_tree_type.BasicNode(
            "MODULE", self.node_query.node_dict["NODE_BLK_MODULE_BODY"], parent)
        module_body_node.node_left = self.syn_module_port(module_body_node)
        module_body_node.node_right = self.syn_module_content(module_body_node)
        return module_body_node

    def syn_module_port(self, parent):
        """ BLK_MODULE_PORT node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_LEFTPAREN"]:
            module_port_node = parsing_tree_type.BasicNode(
                "MODULE", self.node_query.node_dict["NODE_BLK_MODULE_PORT"], parent)
            self.consume_cur_token(1)

        if self.cur_token.token_type != self.token_query.token_dict["TOKEN_RIGHTPAREN"]:
            module_port_node.node_left = self.syn_module_port_list(module_port_node)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_RIGHTPAREN"] and
            self.nxt_token.token_type == self.token_query.token_dict["TOKEN_SEMICOLON"]:
            self.consume_cur_token(2)
            return module_port_node
        else:
            self.error_unexpect_token("module_port")

    def syn_module_port_list(self, parent):
        """ BLK_MODULE_PORT_LIST node handler """
        module_port_list_node = parsing_tree_type.BasicNode(
            "MODULE_PORT_LIST", self.node_query.node_dict["NODE_BLK_MODULE_PORT_LIST"], parent)
        module_port_list_node.node_left = self.syn_module_port_exp(module_port_list_node)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_COMMA"]:
            self.consume_cur_token(1)
            module_port_list_node.node_right = self.syn_module_port_list(module_port_list_node)
        
        return module_port_list_node

    def syn_module_port_exp(self, parent):
        """ BLK_MODULE_PORT_EXP node handler """
        module_port_exp_node = parsing_tree_type.BasicNode(
            "MODULE_PORT_EXP", self.node_query.node_dict["NODE_BLK_MODULE_PORT_EXP"], parent)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_KEYDIR"]:
            module_port_exp_node.node_left = self.syn_iodir(module_port_exp_node)

        module_port_exp_node.node_left = self.syn_signal_exp(module_port_exp_node)
        
        return module_port_exp_node
            
    def syn_iodir(self, parent):
        """ IODIR node handler """
        iodir_node = parsing_tree_type.BasicNode(
            self.cur_token.token_text, self.node_query.node_dict["NODE_EXP_IODIR"], parent)
        return iodir_node

    def syn_signal_exp(self, parent):
        """ SIGNAL_EXP node handler """
        signal_exp_node = parsing_tree_type.BasicNode(
            "SIGNAL_EXP", self.node_query.node_dict["NODE_EXP_SIGNAL"], parent)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_KEYTYPE"] or
            self.cur_token.token_type == self.token_query.token_dict["TOKEN_LEFTBRACKET"]:
            signal_exp_node.node_left = self.syn_signal_type(signal_exp_node)

        signal_exp_node.node_rignt = self.syn_signal_identifier(signal_exp_node)

        return signal_exp_node

    def syn_signal_type(self, parent):
        """ SIGNAL_TYPE node handler """
        signal_type_node = parsing_tree_type.BasicNode(
            "SIGNAL_TYPE", self.node_query.node_dict["NODE_EXP_SIGNAL_TYPE"], parent)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_KEYTYPE"]:
            signal_type_node.node_left = self.syn_keytype(signal_type_node)
        
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_LEFTBRACKET"]:
            signal_type_node.node_right = self.syn_width(signal_type_node)
        
        return signal_type_node

    def syn_keytype(self, parent):
        """ KEYTYPE node handler """
        keytype_node = parsing_tree_type.BasicNode(
            "SIGNAL_TYPE, self.node_query.node_dict["NODE_EXP_KEYTYPE"], parent)
            self.consume_cur_token(1)
        return keytype_node



    def syn_module_content(self, parent):
        """ BLK_MODULE_CONTENT node handler """
        module_content_node = parsing_tree_type.BasicNode()
        return module_content_node
