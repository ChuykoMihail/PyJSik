from lexer.token import Token
from lexer.tokens import tokens
import sys
import re


mtoken = tokens()


def parse(characters):
    mtoken.tokens_array.clear()
    pos = 0
    while pos < len(characters):
        match = None
        for token_expr in mtoken.tokens_regex:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                if tag == "RESERVEDNAME":
                    if characters[match.end(0)] != "(":
                        print(match.end(0))
                        continue
                text = match.group(0)
                if tag:
                    token = Token(text, tag, pos)
                    mtoken.tokens_array.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % characters[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens

def lextableToString(lextable):
    res = ""
    counter = -1
    bracketcounter = 0
    tabscounter = 0
    while(counter < len(lextable)-1):
        counter += 1
        i = lextable[counter]
        if i.type == tokens.tokens_type[2] or i.type == tokens.tokens_type[5] or i.type == tokens.tokens_type[6] or i.type == tokens.tokens_type[7]:
            for j in i.value:
                res += ' ' + j
        elif i.value == "\\n" and lextable[counter+1].value == "\\n":
            continue
        elif i.value == "\\n":
                # and lextable[counter+1].value == "\\t"\
            res += ' ' + i.value
            localtabs = 0
            tmpcounter = counter
            while(lextable[tmpcounter+1].value == "\\t"):
                tmpcounter += 1
                localtabs += 1
            else:
                if lextable[tmpcounter+1].value == "\\n":
                    counter = tmpcounter
                elif localtabs > tabscounter:
                    res += ' ' + "{"*(localtabs-tabscounter)
                    counter = tmpcounter
                    tabscounter = localtabs
                    bracketcounter+=1
                elif localtabs < tabscounter:
                    res += ' ' + "} "*(tabscounter-localtabs)
                    counter = tmpcounter
                    tabscounter = localtabs
                    bracketcounter -= 1
                elif localtabs == tabscounter:
                    counter = tmpcounter
                else:
                    continue

        else:
            res += ' ' + i.value
    if tabscounter > 0:
        res += ' '+"} "*tabscounter
    res = res.replace(" \\n", "")
    return res




    # for i in lextable:
    #     counter += 1
    #     if i.type == tokens.tokens_type[2] or i.type == tokens.tokens_type[5] or i.type == tokens.tokens_type[6] or i.type == tokens.tokens_type[7]:
    #         for j in i.value:
    #             res += ' ' + j
    #     elif i.value == "\\n" and lextable[counter+1].value == "\\n":
    #         continue
    #     elif i.value == "\\n" and lextable[counter+1].value == "\\t":
    #         tmpcounter=counter+1
    #         while(lextable[tmpcounter].value == "\\t")
    #     else:
    #         res += ' ' + i.value
    # return res
