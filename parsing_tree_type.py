"""
parsing_tree_type.py
Basic class and needed dictories of parsing tree
"""

class NodeTypeDict:
    """ needed dictories of nodes """
    node_dict = {}
    node_dict["NODE_EMPTY"] = 0
    node_dict["NODE_VERILOG_FILE"] = node_dict["NODE_EMPTY"] + 1
    node_dict["NODE_BLK_TIMESCALE"] = node_dict["NODE_VERILOG_FILE"] + 1
    node_dict["NODE_BLK_TIMEUNIT"] = node_dict["NODE_BLK_TIMESCALE"] + 1
    node_dict["NODE_BLK_TIMEPRECISION"] = node_dict["NODE_BLK_TIMEUNIT"] + 1
    node_dict["NODE_BLK_DEFINE"] = node_dict["NODE_BLK_TIMEPRECISION"] + 1
    node_dict["NODE_BLK_DEFINE_NAME"] = node_dict["NODE_BLK_DEFINE"] + 1
    node_dict["NODE_BLK_DEFINE_VALUE"] = node_dict["NODE_BLK_DEFINE_NAME"] + 1
    node_dict["NODE_BLK_MODULE"] = node_dict["NODE_BLK_DEFINE_VALUE"] + 1
    node_dict["NODE_BLK_MODULE_NAME"] = node_dict["NODE_BLK_MODULE"] + 1
    node_dict["NODE_BLK_MODULE_BODY"] = node_dict["NODE_BLK_MODULE_NAME"] + 1
    node_dict["NODE_BLK_MODULE_PORT"] = node_dict["NODE_BLK_MODULE_BODY"] + 1
    node_dict["NODE_BLK_MODULE_PORT_LIST"] = node_dict["NODE_BLK_MODULE_PORT"] + 1
    node_dict["NODE_BLK_MODULE_PORT_EXP"] = node_dict["NODE_BLK_MODULE_PORT_LIST"] + 1
    node_dict["NODE_BLK_MODULE_CONTENT"] = node_dict["NODE_BLK_MODULE_PORT_EXP"] + 1
    node_dict["NODE_BLK_PARAM"] = node_dict["NODE_BLK_MODULE_CONTENT"] + 1
    node_dict["NODE_BLK_PARAM_TYPE"] = node_dict["NODE_BLK_PARAM"] + 1
    node_dict["NODE_BLK_PARAM_WIDTH"] = node_dict["NODE_BLK_PARAM_TYPE"] + 1
    node_dict["NODE_BLK_PARAM_EXP"] = node_dict["NODE_BLK_PARAM_WIDTH"] + 1
    node_dict["NODE_BLK_PARAM_EXP_NAME"] = node_dict["NODE_BLK_PARAM_EXP"] + 1
    node_dict["NODE_BLK_PARAM_EXP_VALUE"] = node_dict["NODE_BLK_PARAM_EXP_NAME"] + 1
    node_dict["NODE_BLK_PORT_EXP"] = node_dict["NODE_BLK_PARAM_EXP_VALUE"] + 1
    node_dict["NODE_BLK_SIG_EXP"] = node_dict["NODE_BLK_PORT_EXP"] + 1
    node_dict["NODE_BLK_ASSIGN_EXP"] = node_dict["NODE_BLK_SIG_EXP"] + 1
    node_dict["NODE_BLK_ASSIGN_EXP_LVALUE"] = node_dict["NODE_BLK_ASSIGN_EXP"] + 1
    node_dict["NODE_BLK_ASSIGN_EXP_RVALUE"] = node_dict["NODE_BLK_ASSIGN_EXP_LVALUE"] + 1
    node_dict["NODE_BLK_ALWAYS"] = node_dict["NODE_BLK_ASSIGN_EXP_RVALUE"] + 1
    node_dict["NODE_BLK_ALWAYS_SENSITIVITY"] = node_dict["NODE_BLK_ALWAYS"] + 1
    node_dict["NODE_BLK_ALWAYS_EXP"] = node_dict["NODE_BLK_ALWAYS_SENSITIVITY"] + 1
    node_dict["NODE_BLK_INITIAL"] = node_dict["NODE_BLK_ALWAYS_EXP"] + 1
    node_dict["NODE_BLK_INITIAL_EXP"] = node_dict["NODE_BLK_INITIAL"] + 1
    node_dict["NODE_BLK_SUBMODULE"] = node_dict["NODE_BLK_INITIAL_EXP"] + 1
    node_dict["NODE_BLK_SUBMODULE_SOURCE"] = node_dict["NODE_BLK_SUBMODULE"] + 1
    node_dict["NODE_BLK_SUBMODULE_INSTANCE"] = node_dict["NODE_BLK_SUBMODULE_SOURCE"] + 1
    node_dict["NODE_BLK_SUBMODULE_NAME"] = node_dict["NODE_BLK_SUBMODULE_INSTANCE"] + 1
    node_dict["NODE_BLK_SUBMODULE_PARAM"] = node_dict["NODE_BLK_SUBMODULE_NAME"] + 1
    node_dict["NODE_BLK_SUBMODULE_PARAM_LIST"] = node_dict["NODE_BLK_SUBMODULE_PARAM"] + 1
    node_dict["NODE_BLK_SUBMODULE_PORT"] = node_dict["NODE_BLK_SUBMODULE_PARAM_LIST"] + 1
    node_dict["NODE_BLK_SUBMODULE_PORT_LIST"] = node_dict["NODE_BLK_SUBMODULE_PORT"] + 1
    node_dict["NODE_EXP_IF"] = node_dict["NODE_BLK_SUBMODULE_PORT_LIST"] + 1
    node_dict["NODE_EXP_IF_CONDITION"] = node_dict["NODE_EXP_IF"] + 1
    node_dict["NODE_EXP_IF_TRUE_DO"] = node_dict["NODE_EXP_IF_CONDITION"] + 1
    node_dict["NODE_EXP_IF_ELIF_CONDITION"] = node_dict["NODE_EXP_IF_TRUE_DO"] + 1
    node_dict["NODE_EXP_IF_ELIF_DO"] = node_dict["NODE_EXP_IF_ELIF_CONDITION"] + 1
    node_dict["NODE_EXP_IF_ELSE_DO"] = node_dict["NODE_EXP_IF_ELIF_DO"] + 1
    node_dict["NODE_EXP_CASE"] = node_dict["NODE_EXP_IF_ELSE_DO"] + 1
    node_dict["NODE_EXP_CASE_SOURCE"] = node_dict["NODE_EXP_CASE"] + 1
    node_dict["NODE_EXP_CASE_CONDITION"] = node_dict["NODE_EXP_CASE_SOURCE"] + 1
    node_dict["NODE_EXP_CASE_DO"] = node_dict["NODE_EXP_CASE_CONDITION"] + 1
    node_dict["NODE_EXP_CASE_DEFAULT_DO"] = node_dict["NODE_EXP_CASE_DO"] + 1
    node_dict["NODE_EXP_BLKING_ASSIGN"] = node_dict["NODE_EXP_CASE_DEFAULT_DO"] + 1
    node_dict["NODE_EXP_BLKING_ASSIGN_LVALUE"] = node_dict["NODE_EXP_BLKING_ASSIGN"] + 1
    node_dict["NODE_EXP_BLKING_ASSIGN_RVALUE"] = node_dict["NODE_EXP_BLKING_ASSIGN_LVALUE"] + 1
    node_dict["NODE_EXP_NBLKING_ASSIGN"] = node_dict["NODE_EXP_BLKING_ASSIGN_RVALUE"] + 1
    node_dict["NODE_EXP_NBLKING_ASSIGN_LVALUE"] = node_dict["NODE_EXP_NBLKING_ASSIGN"] + 1
    node_dict["NODE_EXP_NBLKING_ASSIGN_RVALUE"] = node_dict["NODE_EXP_NBLKING_ASSIGN_LVALUE"] + 1
    node_dict["NODE_EXP_VECTOR"] = node_dict["NODE_EXP_NBLKING_ASSIGN_RVALUE"] + 1
    node_dict["NODE_EXP_VECTOR_REMAIN"] = node_dict["NODE_EXP_VECTOR"] + 1
    node_dict["NODE_EXP_NUMBER"] = node_dict["NODE_EXP_VECTOR_REMAIN"] + 1
    node_dict["NODE_EXP_VARIABLE"] = node_dict["NODE_EXP_NUMBER"] + 1
    node_dict["NODE_EXP_KEYWORD"] = node_dict["NODE_EXP_VARIABLE"] + 1
    node_dict["NODE_EXP_KEYUNIT"] = node_dict["NODE_EXP_KEYWORD"] + 1
    node_dict["NODE_EXP_KEYOP"] = node_dict["NODE_EXP_KEYUNIT"] + 1
    node_dict["NODE_EXP_NAME"] = node_dict["NODE_EXP_KEYOP"] + 1
    node_dict["NODE_EXP_IODIR"] = node_dict["NODE_EXP_NAME"] + 1
    node_dict["NODE_EXP_SIGNAL"] = node_dict["NODE_EXP_IODIR"] + 1
    node_dict["NODE_EXP_SIGNAL_TYPE"] = node_dict["NODE_EXP_SIGNAL"] + 1
    node_dict["NODE_EXP_SIGNAL_IDENTIFIER"] = node_dict["NODE_EXP_SIGNAL_TYPE"] + 1
    node_dict["NODE_EXP_KEYTYPE"] = node_dict["NODE_EXP_SIGNAL_IDENTIFIER"] + 1
    node_dict["NODE_EXP_WIDTH"] = node_dict["NODE_EXP_KEYTYPE"] + 1
    node_dict["NODE_EXP_CONNECT"] = node_dict["NODE_EXP_WIDTH"] + 1
    node_dict["NODE_EXP_COLLECT"] = node_dict["NODE_EXP_CONNECT"] + 1


    node_backward_dict = {}
    for key, value in node_dict.items():
        node_backward_dict[value] = key

    def get_node_number(self, type_string):
        """ Return the number of the node type """
        if type_string in self.node_dict:
            return self.node_dict[type_string]

        print("ERROR!! node type string is wrong", type_string)
        quit()


    def get_node_string(self, type_number):
        """ Return the string of the node type """
        if type_number in self.node_backward_dict:
            return self.node_backward_dict[type_number]

        print("ERROR!! node type number is wrong", type_number)
        quit()



class BasicNode:
    """ The base class of node """
    def __init__(self, node_text="", node_type=0, node_parent=None):
        """ Only use binary tree because one verilog file would not create a too big tree """
        self.node_text = node_text
        self.node_type = node_type
        self.node_parent = node_parent
        self.node_left = None
        self.node_right = None

    def get_node_type(self):
        """ return the number of the node type """
        return self.node_type

    def get_node_text(self):
        """ return the string of the node text """
        return self.node_text
