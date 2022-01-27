import sys

from semanticaltree.operationtree import SyntacticsStructure
from semanticaltree.operationtree import NodeStruct


class SemanticalAnalyzer:
    def __init__(self, opertree: SyntacticsStructure):
        self.tree = opertree
        self.root = self.tree.root
        self.variables = []
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
                elif right.name in ["INTEGER", "BOOL", "STRING"]:
                    self.variables.append((left.value, right.name))
                elif right.name == "VARIABLE":
                    if self.checkvarbool(right):
                        var = self.checkvar(right)
                        self.variables.append((left.value, var[1]))
                    else:
                        sys.stderr.write('Unresolved variable: %s\n' % right.value)
                        sys.exit(1)



    def subscantypes(self, operation):
        left = operation.childs[0]
        right = operation.childs[1]
        if (left.name, right.name) in [
            ("INTEGER", "STRING"),
            ("STRING", "INTEGER")
        ]:
            sys.stderr.write('Illegal type: %s\n' % right.name)
            sys.exit(1)
        elif (left.name, right.name) in [
            ("INTEGER", "INTEGER"),
            ("STRING", "STRING")
        ]:
            operation.name = left.name
        elif left.name == "OPERATOR":
            self.subscan(left)
        elif right.name == "OPERATOR":
            self.subscan(right)
        if left.name == "VARIABLE":
            if self.checkvarbool(left):
                var = self.checkvar(left)
                if (var[1], right.name) in [
                    ("INTEGER", "INTEGER"),
                    ("STRING", "STRING")
                ]:
                    operation.name = var[1]
                elif (var[1], right.name) in [
                    ("INTEGER", "STRING"),
                    ("STRING", "INTEGER")
                ]:
                    sys.stderr.write('Illegal type: %s\n' % right.name)
                    sys.exit(1)
            else:
                sys.stderr.write('Unresolved variable: %s\n' % left.value)
                sys.exit(1)
        elif right.name == "VARIABLE":
            if self.checkvarbool(right):
                var = self.checkvar(right)
                if (var[1], left.name) in [
                    ("INTEGER", "INTEGER"),
                    ("STRING", "STRING")
                ]:
                    operation.name = var[1]
                elif (var[1], left.name) in [
                    ("INTEGER", "STRING"),
                    ("STRING", "INTEGER")
                ]:
                    sys.stderr.write('Illegal type: %s\n' % right.name)
                    sys.exit(1)
            else:
                sys.stderr.write('Unresolved variable: %s\n' % left.value)
                sys.exit(1)
