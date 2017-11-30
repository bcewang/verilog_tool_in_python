class token_type_enum:
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
    type_singlequote = type_grave + 1
    #type "
    type_doublequote = type_singlequote + 1
    #type @
    type_at = type_doublequote + 1
    #type +
    type_plus = type_at + 1
    #type -
    type_minus = type_plus + 1
    #type /
    type_slash = type_minus + 1
    #type \
    type_backslash = type_slash + 1
    #type ?
    type_question = type_backslash + 1
    #type !
    type_exclamation = type_question + 1
    #type &
    type_and = type_exclamation + 1
    #type |
    type_or = type_and + 1
    #type ~
    type_not = type_or + 1


class token_class:
    token_text = ""
    token_type = 0

    def __init__(self, text, type):
        self.token_text = text
        self.token_type = type

    def get_token(self):
        return token_text

