import sys

from semanticaltree.operationtree import SyntacticsStructure
from semanticaltree.operationtree import NodeStruct


class SemanticalAnalyzer:
    def __init__(self, opertree: SyntacticsStructure):
        self.tree = opertree
        self.root = self.tree.root
        self.variables = []
        self.scan(self.root)

    def scan(self, ptr: NodeStruct):
        self.scantypes(ptr)
        self.scanvars(ptr)

    def scanvars(self, ptr = None):
        if ptr.name !="VARIABLE":
            for child in ptr.childs:
                self.scanvars(child)
        elif ptr.prev.name == "ASSIGNMENT":
            if ptr.prev.childs[0].value == ptr.value:
                if ptr.prev.childs[1].name in [
                    "INTEGER", "STRING"
                ]:
                    self.variables.append((ptr.value, ptr.prev.childs[1].name))
                elif ptr.prev.childs[1].name == "VARIABLE":
                    for var in self.variables:
                        if ptr.prev.childs[1].value==var[0]:
                            self.variables.append((ptr.value, var[1]))
            elif ptr.value not in self.variables[:][0]:
                sys.stderr.write('Unresolved reference: %s\n' % ptr.value)
                sys.exit(1)


           # if child.name == "VARIABLE":
           #     if ptr.name =="ASSIGNMENT" and ptr.childs[0].value == child.value:



    def scantypes(self, ptr: NodeStruct):
        for child in ptr.childs:
            if (child.name not in ["OPERATOR"]):
                self.scantypes(child)
            else:
                left = child.childs[0]
                right = child.childs[1]
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
                    child.name = left.name
                elif left.name == "OPERATOR":
                    self.subscantypes(left)
                    self.scantypes(child.prev)
                elif right.name == "OPERATOR":
                    self.subscantypes(right)
                    self.scantypes(child.prev)


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
