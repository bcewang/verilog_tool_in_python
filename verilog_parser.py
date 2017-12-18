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
        self.parsing_tree.node_left = self.__syn_verilog_file(self.parsing_tree)
        #self.print_parsing_tree(self.parsing_tree, 0)

    def print_parsing_tree(self, root, level):
        """ Recursive print the text of all nodes """
        new_level = level + 1

        print(root.node_text, end='')
        if root.node_left != None:
            print("\n", " "*level, new_level, "->", end='')
            self.print_parsing_tree(root.node_left, new_level)
        if root.node_right != None:
            print("\n", " "*level, new_level, "-->", end='')
            self.print_parsing_tree(root.node_right, new_level)

    def __error_unexpect_token(self, source, parent_node):
        """ Encounter unexpect token, stop parsing """
        print("ERROR!! Unexpect token when", source, parent_node.node_text,
              self.cur_token.token_type, self.cur_token.token_text,
              self.nxt_token.token_type, self.nxt_token.token_text)
        self.print_parsing_tree(self.parsing_tree, 0)
        quit()

    def consume_cur_token(self, times=1):
        """ Pop the used tokens """
        for _ in range(times):
            self.cur_token = self.nxt_token
            self.nxt_token = self.scanner.get_next_token()

    def __syn_verilog_file(self, parent):
        """ VERILOG_FILE node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_EOF"]:
            vfile_node = parsing_tree_type.BasicNode(
                "EOF", self.node_query.node_dict["NODE_EMPTY"], parent)
            return vfile_node
        else:
            vfile_node = parsing_tree_type.BasicNode(
                "VFILE", self.node_query.node_dict["NODE_VERILOG_FILE"], parent)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_GRAVE"]:
            if self.nxt_token.token_text == "timescale":
                self.consume_cur_token(2)
                vfile_node.node_left = self.__syn_timescale(vfile_node)
            elif self.nxt_token.token_text == "define":
                self.consume_cur_token(2)
                vfile_node.node_left = self.__syn_define(vfile_node)
            else:
                self.__error_unexpect_token("verilog_file1", parent)
        elif self.cur_token.token_text == "module":
            self.consume_cur_token(1)
            vfile_node.node_left = self.__syn_module(vfile_node)
        else:
            self.__error_unexpect_token("verilog_file2", parent)

        vfile_node.node_right = self.__syn_verilog_file(vfile_node)
        return vfile_node

    def __syn_timescale(self, parent):
        """ BLK_TIMESCALE node handler """
        timescale_node = parsing_tree_type.BasicNode(
            "TIMESCALE", self.node_query.node_dict["NODE_BLK_TIMESCALE"], parent)
        timescale_node.node_left = self.__syn_timeunit(timescale_node)
        timescale_node.node_right = self.__syn_timeprecision(timescale_node)
        return timescale_node

    def __syn_timeunit(self, parent):
        """ BLK_TIMEUNIT node handler """
        timeunit_node = parsing_tree_type.BasicNode(
            "TIMEUNIT", self.node_query.node_dict["NODE_BLK_TIMEUNIT"], parent)
        timeunit_node.node_left = self.__syn_number(timeunit_node)
        timeunit_node.node_right = self.__syn_keyunit(timeunit_node)
        return timeunit_node

    def __syn_number(self, parent):
        """ EXP_NUMBER node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_NUMBER"]:
            number_node = parsing_tree_type.BasicNode(
                self.cur_token.token_text, self.node_query.node_dict["NODE_EXP_NUMBER"], parent)
            self.consume_cur_token(1)
            return number_node
        else:
            self.__error_unexpect_token("number", parent)

    def __syn_keyunit(self, parent):
        """ EXP_NUMBER node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_KEYUNIT"]:
            keyunit_node = parsing_tree_type.BasicNode(
                self.cur_token.token_text, self.node_query.node_dict["NODE_EXP_KEYUNIT"], parent)
            self.consume_cur_token(1)
            return keyunit_node
        else:
            self.__error_unexpect_token("keyunit", parent)


    def __syn_timeprecision(self, parent):
        """ BLK_TIMEPRECISION node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_SLASH"]:
            self.consume_cur_token(1)
            timeprecision_node = parsing_tree_type.BasicNode(
                "TIMEPRECISION", self.node_query.node_dict["NODE_BLK_TIMEPRECISION"], parent)
            timeprecision_node.node_left = self.__syn_number(timeprecision_node)
            timeprecision_node.node_right = self.__syn_keyunit(timeprecision_node)
            return timeprecision_node
        else:
            self.__error_unexpect_token("timeprecision", parent)

    def __syn_define(self, parent):
        """ BLK_DEFINE node handler """
        define_node = parsing_tree_type.BasicNode(
            "DEFINE", self.node_query.node_dict["NODE_BLK_DEFINE"], parent)
        if self.cur_token.line_number == self.nxt_token.line_number:
            # cur_token.line_number will change when __syn_name
            define_node.node_left = self.__syn_name(define_node)
            define_node.node_right = self.__syn_define_value(define_node)
        else:
            define_node.node_left = self.__syn_name(define_node)

        return define_node

    def __syn_name(self, parent):
        """ BLK_NAME node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_VARIABLE"]:
            define_name_node = parsing_tree_type.BasicNode(
                self.cur_token.token_text, self.node_query.node_dict["NODE_EXP_NAME"], parent)
            self.consume_cur_token(1)
            return define_name_node
        else:
            self.__error_unexpect_token("name", parent)

    def __syn_define_value(self, parent):
        """ BLK_DEFINE_VALUE node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_NUMBER"]:
            define_value_node = parsing_tree_type.BasicNode(
                self.cur_token.token_text,
                self.node_query.node_dict["NODE_BLK_DEFINE_VALUE"], parent)
            self.consume_cur_token(1)
            return define_value_node
        else:
            self.__error_unexpect_token("define_value", parent)

    def __syn_module(self, parent):
        """ BLK_MODULE node handler """
        module_node = parsing_tree_type.BasicNode(
            "MODULE", self.node_query.node_dict["NODE_BLK_MODULE"], parent)
        module_node.node_left = self.__syn_name(module_node)
        module_node.node_right = self.__syn_module_body(module_node)
        return module_node

    def __syn_module_body(self, parent):
        """ BLK_MODULE_BODY node handler """
        module_body_node = parsing_tree_type.BasicNode(
            "MODULE_BODY", self.node_query.node_dict["NODE_BLK_MODULE_BODY"], parent)
        module_body_node.node_left = self.__syn_module_port(module_body_node)
        module_body_node.node_right = self.__syn_module_content(module_body_node)
        return module_body_node

    def __syn_module_port(self, parent):
        """ BLK_MODULE_PORT node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_LEFTPAREN"]:
            module_port_node = parsing_tree_type.BasicNode(
                "MODULE_PORT", self.node_query.node_dict["NODE_BLK_MODULE_PORT"], parent)
            self.consume_cur_token(1)
        else:
            self.__error_unexpect_token("module_port start", parent)

        if self.cur_token.token_type != self.token_query.token_dict["TOKEN_RIGHTPAREN"]:
            module_port_node.node_left = self.__syn_module_port_list(module_port_node)

        if (self.cur_token.token_type == self.token_query.token_dict["TOKEN_RIGHTPAREN"] and
                self.nxt_token.token_type == self.token_query.token_dict["TOKEN_SEMICOLON"]):
            self.consume_cur_token(2)
            return module_port_node
        else:
            self.__error_unexpect_token("module_port end", parent)

    def __syn_module_port_list(self, parent):
        """ BLK_MODULE_PORT_LIST node handler """
        module_port_list_node = parsing_tree_type.BasicNode(
            "MODULE_PORT_LIST", self.node_query.node_dict["NODE_BLK_MODULE_PORT_LIST"], parent)
        module_port_list_node.node_left = self.__syn_module_port_exp(module_port_list_node)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_COMMA"]:
            self.consume_cur_token(1)
            module_port_list_node.node_right = self.__syn_module_port_list(module_port_list_node)

        return module_port_list_node

    def __syn_module_port_exp(self, parent):
        """ BLK_MODULE_PORT_EXP node handler """
        module_port_exp_node = parsing_tree_type.BasicNode(
            "MODULE_PORT_EXP", self.node_query.node_dict["NODE_BLK_MODULE_PORT_EXP"], parent)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_KEYDIR"]:
            module_port_exp_node.node_left = self.__syn_iodir(module_port_exp_node)

        module_port_exp_node.node_right = self.__syn_signal_exp(module_port_exp_node)

        return module_port_exp_node

    def __syn_iodir(self, parent):
        """ IODIR node handler """
        iodir_node = parsing_tree_type.BasicNode(
            self.cur_token.token_text, self.node_query.node_dict["NODE_EXP_IODIR"], parent)
        self.consume_cur_token(1)
        return iodir_node

    def __syn_signal_exp(self, parent):
        """ SIGNAL_EXP node handler """
        signal_exp_node = parsing_tree_type.BasicNode(
            "SIGNAL_EXP", self.node_query.node_dict["NODE_EXP_SIGNAL"], parent)

        if (self.cur_token.token_type == self.token_query.token_dict["TOKEN_KEYTYPE"] or
                self.cur_token.token_type == self.token_query.token_dict["TOKEN_LEFTBRACKET"]):
            signal_exp_node.node_left = self.__syn_signal_type(signal_exp_node)

        signal_exp_node.node_right = self.__syn_signal_identifier(signal_exp_node)

        return signal_exp_node

    def __syn_signal_type(self, parent):
        """ SIGNAL_TYPE node handler """
        signal_type_node = parsing_tree_type.BasicNode(
            "SIGNAL_TYPE", self.node_query.node_dict["NODE_EXP_SIGNAL_TYPE"], parent)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_KEYTYPE"]:
            signal_type_node.node_left = self.__syn_keytype(signal_type_node)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_LEFTBRACKET"]:
            signal_type_node.node_right = self.__syn_width(signal_type_node)

        return signal_type_node

    def __syn_keytype(self, parent):
        """ KEYTYPE node handler """
        keytype_node = parsing_tree_type.BasicNode(
            self.cur_token.token_text, self.node_query.node_dict["NODE_EXP_KEYTYPE"], parent)
        self.consume_cur_token(1)
        return keytype_node

    def __syn_width(self, parent):
        """ WIDTH node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_LEFTBRACKET"]:
            width_node = parsing_tree_type.BasicNode(
                "WIDTH", self.node_query.node_dict["NODE_EXP_WIDTH"], parent)
            self.consume_cur_token(1)

        width_node.node_left = self.__syn_number(width_node)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_PLUS"]:
            width_node.node_text = "WIDTH+"
            self.consume_cur_token(1)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_COLON"]:
            self.consume_cur_token(1)
        else:
            self.__error_unexpect_token("width colon", parent)

        width_node.node_right = self.__syn_number(width_node)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_RIGHTBRACKET"]:
            self.consume_cur_token(1)
            return width_node
        else:
            self.__error_unexpect_token("width right bracket", parent)

    def __syn_signal_identifier(self, parent):
        """ SIGNAL_IDENTIFIER node handler """
        signal_identifier_node = parsing_tree_type.BasicNode(
            "SIGNAL_IDENTIFIER", self.node_query.node_dict["NODE_EXP_SIGNAL_IDENTIFIER"], parent)
        signal_identifier_node.node_left = self.__syn_name(signal_identifier_node)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_LEFTBRACKET"]:
            signal_identifier_node.node_right = self.__syn_width(signal_identifier_node)

        return signal_identifier_node


    def __syn_module_content(self, parent):
        """ BLK_MODULE_CONTENT node handler """
        module_content_node = parsing_tree_type.BasicNode(
            "MODULE_CONTENT", self.node_query.node_dict["NODE_BLK_MODULE_CONTENT"], parent)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_KEYDIR"]:
            module_content_node.node_left = self.__syn_blk_port_exp(module_content_node)
        elif self.cur_token.token_type == self.token_query.token_dict["TOKEN_KEYTYPE"]:
            module_content_node.node_left = self.__syn_blk_sig_exp(module_content_node)
        elif self.cur_token.token_type == self.token_query.token_dict["TOKEN_VARIABLE"]:
            module_content_node.node_left = self.__syn_submodule(module_content_node)
        elif self.cur_token.token_text == "endmodule":
            self.consume_cur_token(1)
            return module_content_node
        else:
            self.__error_unexpect_token("module content", parent)

        module_content_node.node_right = self.__syn_module_content(module_content_node)
        return module_content_node

    def __syn_blk_port_exp(self, parent):
        """ BLK_PORT_EXP node handler """
        port_exp_node = parsing_tree_type.BasicNode(
            "BLK_PORT_EXP", self.node_query.node_dict["NODE_BLK_PORT_EXP"], parent)
        port_exp_node.node_left = self.__syn_iodir(port_exp_node)
        port_exp_node.node_right = self.__syn_signal_exp(port_exp_node)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_SEMICOLON"]:
            self.consume_cur_token(1)
            return port_exp_node
        else:
            self.__error_unexpect_token("port exp end", parent)

    def __syn_blk_sig_exp(self, parent):
        """ BLK_SIG_EXP node handler """
        sig_exp_node = parsing_tree_type.BasicNode(
            "BLK_SIG_EXP", self.node_query.node_dict["NODE_BLK_SIG_EXP"], parent)
        sig_exp_node.node_left = self.__syn_signal_exp(sig_exp_node)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_SEMICOLON"]:
            self.consume_cur_token(1)
            return sig_exp_node
        else:
            self.__error_unexpect_token("sig exp end", parent)

    def __syn_submodule(self, parent):
        """ SUBMODULE node handler """
        submodule_node = parsing_tree_type.BasicNode(
            "SUBMODULE", self.node_query.node_dict["NODE_BLK_SUBMODULE"], parent)
        submodule_node.node_left = self.__syn_submodule_source(submodule_node)
        submodule_node.node_right = self.__syn_submodule_instance(submodule_node)
        return submodule_node

    def __syn_submodule_source(self, parent):
        """ SUBMODULE SOURCE node handler """
        submodule_source_node = parsing_tree_type.BasicNode(
            self.cur_token.token_text,
            self.node_query.node_dict["NODE_BLK_SUBMODULE_SOURCE"], parent)
        self.consume_cur_token(1)
        return submodule_source_node

    def __syn_submodule_instance(self, parent):
        """ SUBMODULE INSTANCE node handler """
        submodule_instance_node = parsing_tree_type.BasicNode(
            "SUBMODULE_INSTANCE", self.node_query.node_dict["NODE_BLK_SUBMODULE_INSTANCE"], parent)
        submodule_instance_node.node_left = self.__syn_submodule_name(submodule_instance_node)
        submodule_instance_node.node_right = self.__syn_submodule_port(submodule_instance_node)
        return submodule_instance_node

    def __syn_submodule_name(self, parent):
        """ SUBMODULE NAME node handler """
        submodule_name_node = parsing_tree_type.BasicNode(
            "SUBMODULE_NAME", self.node_query.node_dict["NODE_BLK_SUBMODULE_NAME"], parent)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_HASH"]:
            submodule_name_node.node_left = self.__syn_submodule_param(submodule_name_node)

        submodule_name_node.node_right = self.__syn_name(submodule_name_node)

        return submodule_name_node

    def __syn_submodule_param(self, parent):
        """ SUBMODULE PARAM node handler """
        if (self.cur_token.token_type == self.token_query.token_dict["TOKEN_HASH"] and
                self.nxt_token.token_type == self.token_query.token_dict["TOKEN_LEFTPAREN"]):
            submodule_param_node = parsing_tree_type.BasicNode(
                "SUBMODULE_PARAM", self.node_query.node_dict["NODE_BLK_SUBMODULE_PARAM"], parent)
            self.consume_cur_token(2)
        else:
            self.__error_unexpect_token("submodule_param_start", parent)

        submodule_param_node.node_left = self.__syn_submodule_param_list(submodule_param_node)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_RIGHTPAREN"]:
            self.consume_cur_token(1)
            return submodule_param_node
        else:
            self.__error_unexpect_token("submodule_param_end", parent)

    def __syn_submodule_param_list(self, parent):
        """ SUBMODULE PARAM LIST node handler """
        submodule_param_list_node = parsing_tree_type.BasicNode(
            "SUBMODULE_PARAM_LIST",
            self.node_query.node_dict["NODE_BLK_SUBMODULE_PARAM_LIST"], parent)
        submodule_param_list_node.node_left = self.__syn_connect_exp(submodule_param_list_node)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_COMMA"]:
            self.consume_cur_token(1)
            submodule_param_list_node.node_right = self.__syn_submodule_param_list(
                submodule_param_list_node)

        return submodule_param_list_node

    def __syn_connect_exp(self, parent):
        """ CONNECT node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_DOT"]:
            self.consume_cur_token(1)
            connect_exp_node = parsing_tree_type.BasicNode(
                "CONNECT", self.node_query.node_dict["NODE_EXP_CONNECT"], parent)
        else:
            self.__error_unexpect_token("connect_start", parent)

        connect_exp_node.node_left = self.__syn_name(connect_exp_node)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_LEFTPAREN"]:
            self.consume_cur_token(1)
            if self.cur_token.token_type != self.token_query.token_dict["TOKEN_RIGHTPAREN"]:
                connect_exp_node.node_right = self.__syn_vector(connect_exp_node)
        else:
            self.__error_unexpect_token("connect_middle", parent)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_RIGHTPAREN"]:
            self.consume_cur_token(1)
            return connect_exp_node
        else:
            self.__error_unexpect_token("connect_end", parent)

    def __syn_submodule_port(self, parent):
        """ SUBMODULE PORT node handler """
        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_LEFTPAREN"]:
            submodule_port_node = parsing_tree_type.BasicNode(
                "SUBMODULE_PORT", self.node_query.node_dict["NODE_BLK_SUBMODULE_PARAM"], parent)
            self.consume_cur_token(1)
        else:
            self.__error_unexpect_token("submodule_port_start", parent)

        submodule_port_node.node_left = self.__syn_submodule_port_list(submodule_port_node)

        if (self.cur_token.token_type == self.token_query.token_dict["TOKEN_RIGHTPAREN"] and
                self.nxt_token.token_type == self.token_query.token_dict["TOKEN_SEMICOLON"]):
            self.consume_cur_token(2)
            return submodule_port_node
        else:
            self.__error_unexpect_token("submodule_param_end", parent)

    def __syn_submodule_port_list(self, parent):
        """ SUBMODULE PORT LIST node handler """
        submodule_port_list_node = parsing_tree_type.BasicNode(
            "SUBMODULE_PORT_LIST",
            self.node_query.node_dict["NODE_BLK_SUBMODULE_PORT_LIST"], parent)
        submodule_port_list_node.node_left = self.__syn_connect_exp(submodule_port_list_node)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_COMMA"]:
            self.consume_cur_token(1)
            submodule_port_list_node.node_right = self.__syn_submodule_port_list(
                submodule_port_list_node)

        return submodule_port_list_node

    def __syn_vector(self, parent):
        """ VECTOR node handler """
        vector_node = parsing_tree_type.BasicNode(
            "VECTOR", self.node_query.node_dict["NODE_EXP_VECTOR"], parent)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_NUMBER"]:
            vector_node.node_left = self.__syn_number(vector_node)
        elif self.cur_token.token_type == self.token_query.token_dict["TOKEN_VARIABLE"]:
            vector_node.node_left = self.__syn_signal_identifier(vector_node)
        elif self.cur_token.token_type == self.token_query.token_dict["TOKEN_LEFTPAREN"]:
            self.consume_cur_token(1)
            vector_node.node_left = self.__syn_vector(vector_node)
            if self.cur_token.token_type == self.token_query.token_dict["TOKEN_RIGHTPAREN"]:
                self.consume_cur_token(1)
            else:
                self.__error_unexpect_token("vector_rightparen", parent)
        elif self.cur_token.token_type == self.token_query.token_dict["TOKEN_LEFTBRACE"]:
            self.consume_cur_token(1)
            vector_node.node_left = self.__syn_collect(vector_node)
            if self.cur_token.token_type == self.token_query.token_dict["TOKEN_RIGHTBRACE"]:
                self.consume_cur_token(1)
            else:
                self.__error_unexpect_token("vector_rightparen", parent)
        elif self.cur_token.token_type == self.token_query.token_dict["TOKEN_KEYOP"]:
            vector_node.node_left = self.__syn_keyop(vector_node)
        else:
            self.__error_unexpect_token("vector", parent)

        vector_node.node_right = self.__syn_vector_remain(vector_node)

        return vector_node

    def __syn_collect(self, parent):
        """ COLLECT node handler """
        collect_node = parsing_tree_type.BasicNode(
            "COLLECT", self.node_query.node_dict["NODE_EXP_COLLECT"], parent)

        if (self.cur_token.token_type == self.token_query.token_dict["TOKEN_NUMBER"] and
                self.nxt_token.token_type == self.token_query.token_dict["TOKEN_LEFTBRACE"]):
            collect_node.node_left = self.__syn_number(collect_node)
            self.consume_cur_token(1)
            collect_node.node_right = self.__syn_collect(collect_node)
            if self.cur_token.token_type == self.token_query.token_dict["TOKEN_RIGHTBRACE"]:
                self.consume_cur_token(1)
            else:
                self.__error_unexpect_token("vector_rightparen", parent)
        else:
            collect_node.node_left = self.__syn_vector(collect_node)
            if self.cur_token.token_type == self.token_query.token_dict["TOKEN_COMMA"]:
                self.consume_cur_token(1)
                collect_node.node_right = self.__syn_vector(collect_node)

        return collect_node

    def __syn_vector_remain(self, parent):
        """ VECTOR REMAIN node handler """
        vector_remain_node = parsing_tree_type.BasicNode(
            "VECTOR_REMAIN", self.node_query.node_dict["NODE_EXP_VECTOR_REMAIN"], parent)

        if self.cur_token.token_type == self.token_query.token_dict["TOKEN_KEYOP"]:
            vector_remain_node.node_left = self.__syn_keyop(vector_remain_node)

        if (self.cur_token.token_type != self.token_query.token_dict["TOKEN_RIGHTBRACE"] and
                self.cur_token.token_type != self.token_query.token_dict["TOKEN_RIGHTPAREN"] and
                self.cur_token.token_type != self.token_query.token_dict["TOKEN_SEMICOLON"]):
            vector_remain_node.node_right = self.__syn_vector(vector_remain_node)

        return vector_remain_node

    def __syn_keyop(self, parent):
        """ KEYOP node handler """
        keyop_node = parsing_tree_type.BasicNode(
            self.cur_token.token_text, self.node_query.node_dict["NODE_EXP_KEYOP"], parent)
        self.consume_cur_token(1)
        return keyop_node
