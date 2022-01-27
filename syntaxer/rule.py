class Rule:
    def __init__(self, name, *syntaxunit):
        self.name = name
        self.productions = list(syntaxunit)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s -> %s" % (self.name, " | ".join(repr(p) for p in self.productions))

    def add(self, *productions):
        self.productions.extend(productions)