from lexer.token import Token
from lexer.tokens import tokens
import sys
import re

mtoken = tokens()


def parse(characters):
    pos = 0
    while pos < len(characters):
        match = None
        for token_expr in mtoken.tokens_regex:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = Token(text, tag, pos)
                    tokens.tokens_array.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % characters[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens


def lextableToString(lextable):
    res = ""
    for i in lextable:
        if i.type == tokens.tokens_type[2] or i.type == tokens.tokens_type[5] or i.type == tokens.tokens_type[6] or i.type == tokens.tokens_type[7]:
            for j in i.value:
                res += ' ' + j
        else:
            res += ' ' + i.value
    return res
