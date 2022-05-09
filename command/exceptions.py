
class LexError(Exception):
    """
    Raised when a lexeme is invalid
    """
    pass


class ParsingError(Exception):
    """
    Raised when a series of tokens don't conform to any abstract syntax tree
    """
    pass
