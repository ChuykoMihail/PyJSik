from .rule import Rule
from .sintaxunit import SyntaxUnit


class Grammar:

    def __init__(self):
        self.LETTER = Rule("LETTER", SyntaxUnit("A"), SyntaxUnit("B"), SyntaxUnit("C"), SyntaxUnit("D"),
                           SyntaxUnit("E"), SyntaxUnit("F"), SyntaxUnit("G"), SyntaxUnit("H"), SyntaxUnit("I"),
                           SyntaxUnit("J"), SyntaxUnit("K"), SyntaxUnit("L"), SyntaxUnit("M"), SyntaxUnit("N"),
                           SyntaxUnit("O"), SyntaxUnit("P"), SyntaxUnit("Q"), SyntaxUnit("R"), SyntaxUnit("S"),
                           SyntaxUnit("T"), SyntaxUnit("U"), SyntaxUnit("V"), SyntaxUnit("W"), SyntaxUnit("X"),
                           SyntaxUnit("Y"), SyntaxUnit("Z"),
                           SyntaxUnit("a"), SyntaxUnit("b"), SyntaxUnit("c"), SyntaxUnit("d"), SyntaxUnit("e"),
                           SyntaxUnit("f"), SyntaxUnit("g"), SyntaxUnit("h"), SyntaxUnit("i"), SyntaxUnit("j"),
                           SyntaxUnit("k"), SyntaxUnit("l"), SyntaxUnit("m"), SyntaxUnit("n"), SyntaxUnit("o"),
                           SyntaxUnit("p"), SyntaxUnit("q"), SyntaxUnit("r"), SyntaxUnit("s"), SyntaxUnit("t"),
                           SyntaxUnit("u"), SyntaxUnit("v"), SyntaxUnit("w"), SyntaxUnit("x"), SyntaxUnit("y"),
                           SyntaxUnit("z"))

        self.NOT_NULL_DIGIT = Rule("NOT_NULL_DIGIT", SyntaxUnit("1"), SyntaxUnit("2"), SyntaxUnit("3"), SyntaxUnit("4"),
                                   SyntaxUnit("5"),
                                   SyntaxUnit("6"), SyntaxUnit("7"), SyntaxUnit("8"), SyntaxUnit("9"))

        self.DIGIT = Rule("DIGIT", SyntaxUnit("0"), SyntaxUnit(self.NOT_NULL_DIGIT))

        self.SYMBOL = Rule("SYMBOL", SyntaxUnit("!"), SyntaxUnit("_"), SyntaxUnit("\n"),
                           SyntaxUnit("#"), SyntaxUnit("$"), SyntaxUnit("%"), SyntaxUnit("&"),
                           SyntaxUnit("'"), SyntaxUnit("("), SyntaxUnit(")"), SyntaxUnit("*"),
                           SyntaxUnit("+"), SyntaxUnit("-"), SyntaxUnit("."), SyntaxUnit(","),
                           SyntaxUnit("/"), SyntaxUnit(":"), SyntaxUnit(";"), SyntaxUnit("<"),
                           SyntaxUnit("="), SyntaxUnit(">"), SyntaxUnit("?"), SyntaxUnit("^"),
                           SyntaxUnit("_"), SyntaxUnit("{"), SyntaxUnit("}"), SyntaxUnit("|"),
                           SyntaxUnit("~"), SyntaxUnit(self.DIGIT), SyntaxUnit(self.LETTER))

        self.STRING = Rule("STRING", SyntaxUnit(self.SYMBOL))
        self.STRING.add(SyntaxUnit(self.SYMBOL, self.STRING))

        self.STRING_TYPE = Rule("STRING_TYPE", SyntaxUnit("\"", self.STRING, "\""))

        self.BOOL = Rule("BOOL", SyntaxUnit("True"), SyntaxUnit("False"))

        self.NUM = Rule("NUM", SyntaxUnit(self.DIGIT))
        self.NUM.add(SyntaxUnit(self.DIGIT, self.NUM))

        self.INTEGER = Rule("INTEGER", SyntaxUnit(self.NUM), SyntaxUnit("-", self.NUM))

        self.RELATIONS = Rule("RELATIONS", SyntaxUnit("<"), SyntaxUnit(">"), SyntaxUnit("<="),
                              SyntaxUnit(">="), SyntaxUnit("=="), SyntaxUnit("!="))

        self.ASSIGNMENT_RELATION = Rule("ASSIGNMENT_RELATION", SyntaxUnit("="))

        self.LOGICAL_OPERATOR = Rule("LOGICAL_OPERATOR", SyntaxUnit("or"), SyntaxUnit("and"))

        self.ADDICTIVE_OPERATION = Rule("ADDICTIVE_OPERATION", SyntaxUnit("+"), SyntaxUnit("-"))

        self.MULTIPLICATIVE_OPERATION = Rule("MULTIPLICATIVE_OPERATION", SyntaxUnit("*"), SyntaxUnit("/"))

        self.DIGIT_VAR = Rule("DIGIT_VAR", SyntaxUnit(self.DIGIT))
        self.VARIABLE = Rule("VARIABLE", SyntaxUnit("_", self.DIGIT_VAR),
                             SyntaxUnit(self.LETTER, self.DIGIT_VAR),
                             SyntaxUnit(self.LETTER))
        self.DIGIT_VAR.add(SyntaxUnit(self.DIGIT, self.DIGIT_VAR), SyntaxUnit(self.DIGIT, self.VARIABLE))
        self.VARIABLE.add(SyntaxUnit("_", self.VARIABLE), SyntaxUnit(self.LETTER, self.VARIABLE))

        self.EXP = Rule("EXP", SyntaxUnit("e+"), SyntaxUnit("e-"), SyntaxUnit("E+"),
                        SyntaxUnit("E-"), SyntaxUnit("e"), SyntaxUnit("E"))
        self.REAL_NUMBER = Rule("REAL_NUMBER", SyntaxUnit(self.NUM, ".", self.NUM),
                                SyntaxUnit(self.NUM, ".", self.NUM, self.EXP, self.NUM),
                                SyntaxUnit(self.NUM, ".", self.EXP, self.NUM),
                                SyntaxUnit(self.NUM, self.EXP, self.NUM),
                                SyntaxUnit(".", self.NUM),
                                SyntaxUnit(".", self.NUM, self.EXP, self.NUM)
                                )

        self.FLOAT = Rule("FLOAT", SyntaxUnit(self.REAL_NUMBER), SyntaxUnit("-", self.REAL_NUMBER))

        self.IDENTIFIER = Rule("IDENTIFIER", SyntaxUnit(self.INTEGER), SyntaxUnit(self.STRING_TYPE),
                               SyntaxUnit(self.BOOL),
                               SyntaxUnit(self.VARIABLE), SyntaxUnit(self.FLOAT))

        self.VALUE = Rule("VALUE", SyntaxUnit(self.IDENTIFIER))

        self.RELATION_EXPR = Rule("RELATION_EXPR", SyntaxUnit(self.VALUE))
        self.RELATION_EXPR.add(SyntaxUnit("not", self.RELATION_EXPR))
        self.MULTIPLIER = Rule("MULTIPLIER", SyntaxUnit(self.RELATION_EXPR), SyntaxUnit("(", self.RELATION_EXPR, ")"))
        self.SUMMAND = Rule("SUMMAND", SyntaxUnit(self.MULTIPLIER))
        self.SUMMAND.add(SyntaxUnit(self.SUMMAND, self.MULTIPLICATIVE_OPERATION, self.SUMMAND))

        self.EXPRESSION = Rule("EXPRESSION", SyntaxUnit(self.SUMMAND))
        self.EXPRESSION.add(SyntaxUnit(self.EXPRESSION, self.ADDICTIVE_OPERATION, self.EXPRESSION))
        self.RELATION_EXPR.add(SyntaxUnit(self.EXPRESSION, self.RELATIONS, self.EXPRESSION))
        self.VALUE.add(SyntaxUnit(self.EXPRESSION))

        self.EXPRESSION.add(SyntaxUnit("math.cos", "(", self.VALUE, ")"), SyntaxUnit("math.sin", "(", self.VALUE, ")"),
                            SyntaxUnit("math.sqrt", "(", self.VALUE, ")"), SyntaxUnit("abs", "(", self.VALUE, ")"),
                            SyntaxUnit("math.tan", "(", self.VALUE, ")"))

        self.N = Rule("N", SyntaxUnit("\\n"))
        self.N.add(SyntaxUnit("\\n", self.N))

        self.T = Rule("T", SyntaxUnit("\\t"))
        self.T.add(SyntaxUnit("\\t", self.T))

        self.VARIABLE_DECLARATION = Rule("VARIABLE_DECLARATION",
                                         SyntaxUnit(self.VARIABLE, self.ASSIGNMENT_RELATION, self.VALUE))
        self.COMPOUND_OPERATOR = Rule("COMPOUND_OPERATOR", SyntaxUnit(self.VARIABLE_DECLARATION))

        self.ADDITIONAL_EXPRESSION = Rule("ADDITIONAL_EXPRESSION", SyntaxUnit(self.LOGICAL_OPERATOR,
                                                                              self.RELATION_EXPR))
        self.ADDITIONAL_EXPRESSION.add(SyntaxUnit(self.LOGICAL_OPERATOR, self.RELATION_EXPR,
                                                    self.ADDITIONAL_EXPRESSION))

        self.CONDITIONAL_EXPRESSION = Rule("CONDITIONAL_EXPRESSION", SyntaxUnit(self.RELATION_EXPR),
                                           SyntaxUnit(self.RELATION_EXPR, self.ADDITIONAL_EXPRESSION))

        self.INTERNAL_OPERATOR = Rule("INTERNAL_OPERATOR", SyntaxUnit(self.T, self.COMPOUND_OPERATOR))
        self.INTERNAL_OPERATOR.add(SyntaxUnit(self.T, self.COMPOUND_OPERATOR, self.N, self.INTERNAL_OPERATOR))

        self.WHILE = Rule("WHILE", SyntaxUnit("while", self.CONDITIONAL_EXPRESSION, ":", self.N,
                                              self.INTERNAL_OPERATOR),
                          SyntaxUnit("while", self.CONDITIONAL_EXPRESSION, ":", self.N, self.INTERNAL_OPERATOR,
                                     "else", ":", self.N, self.INTERNAL_OPERATOR))

        self.CONDITIONAL_OPERATOR = Rule("CONDITIONAL_OPERATOR", SyntaxUnit("if", self.CONDITIONAL_EXPRESSION, ":", self.N,
                                                                            self.INTERNAL_OPERATOR),
                                         SyntaxUnit("if", self.CONDITIONAL_EXPRESSION, ":", self.N, self.INTERNAL_OPERATOR,
                                                    self.N, "else", ":", self.N, self.INTERNAL_OPERATOR),
                                         SyntaxUnit("if", self.CONDITIONAL_EXPRESSION, ":", self.N, self.INTERNAL_OPERATOR,
                                                    self.N, self.T, "else", ":", self.N, self.INTERNAL_OPERATOR))

        self.COMPOUND_OPERATOR.add(SyntaxUnit(self.CONDITIONAL_OPERATOR), SyntaxUnit(self.WHILE))
        self.PRINT = Rule("PRINT", SyntaxUnit("print", "(", self.VALUE, ")"))
        self.COMPOUND_OPERATOR.add(SyntaxUnit(self.PRINT))

        self.PROGRAMM = Rule("PROGRAMM", SyntaxUnit(self.COMPOUND_OPERATOR))
        self.PROGRAMM.add(SyntaxUnit(self.COMPOUND_OPERATOR, self.N, self.PROGRAMM))
        self.PROGRAMM.add(SyntaxUnit(self.N, self.PROGRAMM))

        self.GAMMA_RULE = u"GAMMA"
