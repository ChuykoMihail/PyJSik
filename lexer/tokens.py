from .token import Token

class tokens:
    tokens_type = [
        "KEYWORD",  # 0   +
        "RESERVEDNAME",  # 1   +
        "IDENTIFIER",  # 2   +!
        "OPERATOR",  # 3   +
        "SEPARATOR",  # 4   +
        "STRING",  # 5   +!
        "INTEGERNUMBER",  # 6   +!
        "REALNUMBER"  # 7   +!
    ]



    tokens_array: Token = []

    # op = [
    #     "=",    #0
    #     "==",   #1
    #     "!=",   #2
    #     "<=",   #3
    #     ">=",   #4
    #     "+",    #5
    #     "-",    #6
    #     "*",    #7
    #     "/",    #8
    #     ">",    #9
    #     "<",    #10
    #     "and",  #11
    #     "or",   #12
    #     "not"   #13
    # ]

    tokens_regex = [
        (r'\=\=', tokens_type[3]),
        (r'\!\=', tokens_type[3]),
        (r'\<\=', tokens_type[3]),
        (r'\>\=', tokens_type[3]),
        (r'\=', tokens_type[3]),
        (r'\+', tokens_type[3]),
        (r'\-', tokens_type[3]),
        (r'\*', tokens_type[3]),
        (r'\/', tokens_type[3]),
        (r'\>', tokens_type[3]),
        (r'\<', tokens_type[3]),
        (r'and', tokens_type[3]),
        (r'or', tokens_type[3]),
        (r'not', tokens_type[3]),
        (r'\.', tokens_type[4]),
        (r'\:', tokens_type[4]),
        (r'\(', tokens_type[4]),
        (r'\)', tokens_type[4]),
        (r'abs', tokens_type[1]),
        (r'cos', tokens_type[1]),
        (r'sin', tokens_type[1]),
        (r'False', tokens_type[1]),
        (r'True', tokens_type[1]),
        (r'if', tokens_type[0]),
        (r'else', tokens_type[0]),
        (r'\\n', tokens_type[4]),
        (r'\\t+', tokens_type[4]),
        (r'\d+\.[0-9]+', tokens_type[7]),
        (r'\d+', tokens_type[6]),
        (r'\"[A-Za-z0-9_!"№;%:?*()_+ ][A-Za-z0-9_ !"№;%:?*()_+]*\"', tokens_type[5]),
        (r'\'[A-Za-z0-9_!"№;%:?*()_+ ][A-Za-z0-9_ !"№;%:?*()_+]*\'', tokens_type[5]),
        (r'[A-Za-z0-9_]*[A-Za-z0-9_]', tokens_type[2]),
    ]
