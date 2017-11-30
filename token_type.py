"""
token_type.py
Basic class and needed dictories of tokens
"""

class TokenTypeDict:
    """ needed dictories of tokens """
    token_dict = {}
    # token EOF
    token_dict["TOKEN_EOF"] = 0
    # token :
    token_dict["TOKEN_COLON"] = token_dict["TOKEN_EOF"] + 1
    # token ;
    token_dict["TOKEN_SEMICOLON"] = token_dict["TOKEN_COLON"] + 1
    #token (
    token_dict["TOKEN_LEFTPAREN"] = token_dict["TOKEN_SEMICOLON"] + 1
    #token )
    token_dict["TOKEN_RIGHTPAREN"] = token_dict["TOKEN_LEFTPAREN"] + 1
    #token {
    token_dict["TOKEN_LEFTBRACE"] = token_dict["TOKEN_RIGHTPAREN"] + 1
    #token }
    token_dict["TOKEN_RIGHTBRACE"] = token_dict["TOKEN_LEFTBRACE"] + 1
    #token [
    token_dict["TOKEN_LEFTBRACKET"] = token_dict["TOKEN_RIGHTBRACE"] + 1
    #token ]
    token_dict["TOKEN_RIGHTBRACKET"] = token_dict["TOKEN_LEFTBRACKET"] + 1
    #token"] =
    token_dict["TOKEN_EQUAL"] = token_dict["TOKEN_RIGHTBRACKET"] + 1
    #token .
    token_dict["TOKEN_DOT"] = token_dict["TOKEN_EQUAL"] + 1
    #token `
    token_dict["TOKEN_GRAVE"] = token_dict["TOKEN_DOT"] + 1
    #token '
    token_dict["TOKEN_SINGLEQUOTE"] = token_dict["TOKEN_GRAVE"] + 1
    #token "
    token_dict["TOKEN_DOUBLEQUOTE"] = token_dict["TOKEN_SINGLEQUOTE"] + 1
    #token @
    token_dict["TOKEN_AT"] = token_dict["TOKEN_DOUBLEQUOTE"] + 1
    #token +
    token_dict["TOKEN_PLUS"] = token_dict["TOKEN_AT"] + 1
    #token -
    token_dict["TOKEN_MINUS"] = token_dict["TOKEN_PLUS"] + 1
    #token /
    token_dict["TOKEN_SLASH"] = token_dict["TOKEN_MINUS"] + 1
    #token \
    token_dict["TOKEN_BACKSLASH"] = token_dict["TOKEN_SLASH"] + 1
    #token ?
    token_dict["TOKEN_QUESTION"] = token_dict["TOKEN_BACKSLASH"] + 1
    #token !
    token_dict["TOKEN_EXCLAMATION"] = token_dict["TOKEN_QUESTION"] + 1
    #token &
    token_dict["TOKEN_AND"] = token_dict["TOKEN_EXCLAMATION"] + 1
    #token |
    token_dict["TOKEN_OR"] = token_dict["TOKEN_AND"] + 1
    #token ~
    token_dict["TOKEN_NOT"] = token_dict["TOKEN_OR"] + 1

    token_backward_dict = {}
    for key, value in token_dict.items():
        token_backward_dict[value] = key

    symbol_dict = {}
    symbol_dict[":"] = "TOKEN_COLON"
    symbol_dict[";"] = "TOKEN_SEMICOLON"
    symbol_dict["("] = "TOKEN_LEFTPAREN"
    symbol_dict[")"] = "TOKEN_RIGHTPAREN"
    symbol_dict["{"] = "TOKEN_LEFTBRACE"
    symbol_dict["}"] = "TOKEN_RIGHTBRACE"
    symbol_dict["["] = "TOKEN_LEFTBRACKET"
    symbol_dict["]"] = "TOKEN_RIGHTBRACKET"
    symbol_dict["="] = "TOKEN_EQUAL"
    symbol_dict["."] = "TOKEN_DOT"
    symbol_dict["`"] = "TOKEN_GRAVE"
    symbol_dict["'"] = "TOKEN_SINGLEQUOTE"
    symbol_dict['"'] = "TOKEN_DOUBLEQUOTE"
    symbol_dict["@"] = "TOKEN_AT"
    symbol_dict["+"] = "TOKEN_PLUS"
    symbol_dict["-"] = "TOKEN_MINUS"
    symbol_dict["/"] = "TOKEN_SLASH"
    symbol_dict["\\"] = "TOKEN_BACKSLASH"
    symbol_dict["?"] = "TOKEN_QUESTION"
    symbol_dict["!"] = "TOKEN_EXCLAMATION"
    symbol_dict["&"] = "TOKEN_AND"
    symbol_dict["|"] = "TOKEN_OR"
    symbol_dict["~"] = "TOKEN_NOT"

    def get_symbol_type(self, symbol):
        """ Return the number of the token type, or return 999 if it is not a token """
        if symbol in self.symbol_dict:
            return self.token_dict[self.symbol_dict[symbol]]
        return 999

    def get_token_string(self, type_number):
        """ Return the string of the token """
        if type_number in self.token_backward_dict:
            return self.token_backward_dict[type_number]

        print("ERROR!! token type number is wrong", type_number)
        quit()



class BasicToken:
    """ The base class of token """
    token_text = ""
    token_type = 0

    def __init__(self, token_text, token_type):
        self.token_text = token_text
        self.token_type = token_type

    def get_token_type(self):
        """ return the number of the token type """
        return self.token_type

    def get_token_text(self):
        """ return the string of the token text """
        return self.token_text
