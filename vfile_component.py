"""
verilog_class.py
Basic class for verilog syntaxer
"""

class VFile:
    """ The class of verilog file """
    def __init__(self, name):
        self.file_name = name
        self.timeunit = ""
        self.timeprecision = ""
        self.define_dict = {}
        self.module_list = []

    def update_timescale(self, unit, precision):
        """ Update the timescale """
        self.timeunit = unit
        self.timeprecision = precision

    def add_define(self, define_key, define_value):
        """ Add a new define """
        self.define_dict[define_key] = define_value

    def add_module(self, module_node):
        """ Add a new module """
        self.module_list.append(module_node)

    def dump(self):
        """ Dump the content of this file instance """
        print("File Name:", self.file_name)
        print("Time Unit:", self.timeunit)
        print("Time Precision:", self.timeprecision)
        print(self.define_dict)
        for module in self.module_list:
            module.dump()

class VModule:
    """ The class of verilog module """
    def __init__(self, name):
        self.module_name = name
        self.signal_dict = {"input" : [], "output" : [], "inout": [], "net" : []}
        self.submodule_list = []
        self.assign_list = []
        self.always_list = []

    def add_signal(self, signal_type, signal_node):
        """ Add a new signal """
        if signal_type != "net":
            for check_node in self.signal_dict["net"]:
                if check_node.signal_name == signal_node.signal_name:
                    self.signal_dict["net"].remove(check_node)

        self.signal_dict[signal_type].append(signal_node)

    def add_submodule(self, submodule_node):
        """ Add a new submodule """
        self.submodule_list.append(submodule_node)

    def add_assign(self, assign_node):
        """ Add a new assign """
        self.assign_list.append(assign_node)

    def add_always(self, always_node):
        """ Add a new always """
        self.always_list.append(always_node)

    def dump(self):
        """ Dump the content of this module instance """
        print("Module Name:", self.module_name)
        for signal in self.signal_dict["input"]:
            print("input: ", end="")
            signal.dump()
        for signal in self.signal_dict["output"]:
            print("output: ", end="")
            signal.dump()
        for signal in self.signal_dict["inout"]:
            print("inout: ", end="")
            signal.dump()
        for signal in self.signal_dict["net"]:
            signal.dump()
        for submodule in self.submodule_list:
            submodule.dump()

class VSignal:
    """ The class of signal """
    def __init__(self, name, net_type, signal_width=0, array_width=0):
        self.signal_name = name
        self.net_type = net_type
        self.signal_width = signal_width
        self.array_width = array_width

    def dump(self):
        """ Dump the content of this signal instance """
        print(self.net_type, " [", self.signal_width, ":0]  ",
              self.signal_name, "[0:", self.array_width, "]")

class VSubmodule:
    """ The class of submodule """
    def __init__(self, source_name):
        self.source_name = source_name
        self.instance_name = ""
        self.param_list = []
        self.connect_list = []

    def update_instance_name(self, instance_name):
        """ Update the instance name"""
        self.instance_name = instance_name

    def add_param(self, param_node):
        """ Add a new parameter """
        self.param_list.append(param_node)

    def add_connect(self, connect_node):
        """ Add a new connection """
        self.connect_list.append(connect_node)

    def dump(self):
        """ Dump the content of this submodule instance """
        print("SubModule Source Name:", self.source_name)
        print("SubModule Instance Name:", self.instance_name)
        for param in self.param_list:
            param.dump()
        for connect in self.connect_list:
            connect.dump()

class VConnect:
    """ The class of connection """
    def __init__(self, name, vector):
        self.connect_name = name
        self.connect_vector = vector

    def dump(self):
        """ Dump the content of this connect instance """
        print(self.connect_name, self.connect_vector)
