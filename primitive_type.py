class token_type:
    # type EOF
    type_endofstram = 0
    # type :
    type_colon = type_endofstram + 1
    # type ;
    type_semicolon = type_colon + 1
    #type (
    type_leftparen = type_semicolon + 1
    #type )
    type_rightparen = type_leftparen + 1
    #type {
    type_leftbrace = type_rightparen + 1
    #type }
    type_rightbrace = type_leftbrace + 1
    #type [
    type_leftbracket = type_rightbrace + 1
    #type ]
    type_rightbracket = type_leftbracket + 1
    #type =
    type_equal = type_rightbracket + 1
    #type .
    type_dot = type_equal + 1
    #type `
    type_grave = type_dot + 1
    #type '
    type_quote = type_grave + 1
    #type @
    type_at = type_quote + 1


class token_base:
    token_text = ""

    def __init__(self):  
        raise NotImplementedError("primitive is abstract") 

    def get_token(self):
        return token_text



     