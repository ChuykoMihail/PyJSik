import sys

from semanticaltree.operationtree import SyntacticsStructure
from semanticaltree.operationtree import NodeStruct


class SemanticalAnalyzer:
    def __init__(self, opertree: SyntacticsStructure):
        self.tree = opertree
        self.root = self.tree.root
        self.variables = []
        # self.legalcombination = [
        #     ("INTEGER", "INTEGER"),
        #     ("STRING", "STRING"),
        #     ("INTEGER", "BOOL"),
        #     ("BOOL", "INTEGER"),
        #     ("FLOAT", "INTEGER"),
        #     ("INTEGER", "FLOAT"),
        #     ("FLOAT", "FLOAT"),
        #     ("EXPRESSION", "EXPRESSION"),
        #     ("EXPRESSION", "FLOAT"),
        #     ("FLOAT", "EXPRESSION"),
        #     ("EXPRESSION", "INTEGER"),
        #     ("INTEGER", "EXPRESSION")
        # ]
        self.illegalcombination = [
            ("INTEGER", "STRING"),
            ("STRING", "INTEGER"),
            ("EXPRESSION", "STRING"),
            ("STRING", "EXPRESSION"),
            ("STRING", "FLOAT"),
            ("FLOAT", "STRING")
        ]
        self.scan(self.root)



    def checkvar(self, varptr):
        for var in self.variables:
            if varptr.value == var[0]:
                return var

    def checkvarbool(self, varptr):
        for var in self.variables:
            if varptr.value == var[0]:
                return True
        else: return False

    def scan(self, ptr: NodeStruct):
        if ptr.name not in ["ASSIGNMENT"]:
            for child in ptr.childs:
                self.scan(child)
        else:
            left = ptr.childs[0]
            right = ptr.childs[1]
            if left.name == "VARIABLE":
                if right.name == "OPERATOR":
                    self.subscantypes(right)
                    self.scan(ptr.prev)
                elif right.name in ["INTEGER", "BOOL", "STRING", "FLOAT"]:
                    self.variables.append((left.value, right.name))
                elif right.name in ["EXPRESSION"]:
                    self.scanexpression(right)
                elif right.name == "VARIABLE":
                    if self.checkvarbool(right):
                        var = self.checkvar(right)
                        self.variables.append((left.value, var[1]))
                    else:
                        sys.stderr.write('Unresolved variable: %s\n' % right.value)
                        sys.exit(1)

    def scanexpression(self, ptr):
        if ptr.childs[1].name == "VARIABLE":
            if not self.checkvarbool(ptr.childs[1]):
                sys.stderr.write('Unresolved variable: %s\n' % ptr.childs[1].value)
                sys.exit(1)
            elif self.checkvar(ptr.childs[1])[1] == "STRING":
                sys.stderr.write('Expected type \'SupportsFloat\': %s\n' % ptr.childs[0].name)
                sys.exit(1)
        self.variables.append((ptr.prev.childs[0].value, "FLOAT"))


    def subscantypes(self, operation):
        left = operation.childs[0]
        right = operation.childs[1]
        if (left.name, right.name) in self.illegalcombination:
            sys.stderr.write('Illegal type: %s\n' % right.name)
            sys.exit(1)
        elif left.name == "OPERATOR":
            self.subscantypes(left)
        elif right.name == "OPERATOR":
            self.subscantypes(right)
        if left.name == "VARIABLE":
            if self.checkvarbool(left):
                var = self.checkvar(left)
                if (var[1], right.name) in self.illegalcombination:
                    sys.stderr.write('Illegal type: %s\n' % right.name)
                    sys.exit(1)
                elif right.name == "VARIABLE":
                    if self.checkvarbool(right):
                        var2 = self.checkvar(right)
                        if (var[1], var2[1]) in self.illegalcombination:
                            sys.stderr.write('Illegal type: %s\n' % var2[0])
                            sys.exit(1)
                        elif (var[1], var2[1]) not in self.illegalcombination:
                            operation.name = var[1]
                    else:
                        sys.stderr.write('Unresolved variable: %s\n' % left.value)
                        sys.exit(1)
                elif (var[1], right.name) not in self.illegalcombination:
                    operation.name = var[1]
            else:
                sys.stderr.write('Unresolved variable: %s\n' % left.value)
                sys.exit(1)
        elif right.name == "VARIABLE":
            if self.checkvarbool(right):
                var = self.checkvar(right)
                if (var[1], left.name) not in self.illegalcombination:
                    operation.name = var[1]
                elif (var[1], left.name) in self.illegalcombination:
                    sys.stderr.write('Illegal type: %s\n' % right.name)
                    sys.exit(1)
            else:
                sys.stderr.write('Unresolved variable: %s\n' % left.value)
                sys.exit(1)
        elif (left.name, right.name) not in self.illegalcombination:
            operation.name = left.name

