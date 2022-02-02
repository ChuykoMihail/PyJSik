import sys

from semanticaltree.operationtree import SyntacticsStructure
from semanticaltree.operationtree import NodeStruct

class Scope:
    def __init__(self, level, prev):
        self.level = level
        self.variables = []
        self.subscope: list(Scope) = []
        self.prev = prev

    def addvar(self, var):
        self.variables.append(var)

    def checkvarbool(self, varptr):
        for var in self.variables:
            if var[0] == varptr.value:
                return True
        return False

    def checkvar(self, varptr):
        for var in self.variables:
            if var[0] == varptr.value:
                return var
        return None

    def newscope(self):
        newscope = Scope(self.level+1, self)
        self.subscope.append(newscope)
        return newscope


class SemanticalAnalyzer:
    def __init__(self, opertree: SyntacticsStructure):
        self.tree = opertree
        self.root = self.tree.root
        self.scopes = []
        self.illegalcombination = [
            ("INTEGER", "STRING"),
            ("STRING", "INTEGER"),
            ("EXPRESSION", "STRING"),
            ("STRING", "EXPRESSION"),
            ("STRING", "FLOAT"),
            ("FLOAT", "STRING")
        ]
        self.rootscope = Scope(0, None)
        self.currentscope = self.rootscope
        self.scopes.append(self.rootscope)
        self.scan(self.root)

    def checkvar(self, varptr, currscope:Scope):
        for var in currscope.variables:
            if var[0] == varptr.value:
                return var
        else:
            for scope in currscope.subscope:
                if scope.level > self.currentscope.level:
                    return None
                elif scope.level < self.currentscope.level:
                    return self.checkvar(varptr, scope)
                elif scope == self.currentscope:
                    return self.checkvar(varptr, scope)
        return None

    def checkvarbool(self, varptr, currscope):
        for var in currscope.variables:
            if var[0] == varptr.value:
                return True
        else:
            for scope in currscope.subscope:
                if scope.level > self.currentscope.level:
                    return False
                elif scope.level < self.currentscope.level:
                    return self.checkvarbool(varptr, scope)
                elif scope == self.currentscope:
                    return self.checkvarbool(varptr, scope)
        return False

    def scantypes(self, ptr, left, right):
        if right.name == "OPERATOR":
            self.subscantypes(right)
            self.scan(ptr.prev)
        elif right.name in ["INTEGER", "BOOL", "STRING", "FLOAT"]:
            return (left.value, right.name)
        elif right.name in ["EXPRESSION"]:
            if self.scanexpression(right):
                return (right.prev.childs[0].value, "FLOAT")
        elif right.name == "VARIABLE":
            if self.checkvarbool(right, self.rootscope):
                var = self.checkvar(right, self.rootscope)
                return (left.value, var[1])
            else:
                sys.stderr.write('Unresolved variable: %s\n' % right.value)
                sys.exit(1)

    def scanassignment(self, ptr: NodeStruct):
        left = ptr.childs[0]
        right = ptr.childs[1]
        var = self.scantypes(ptr, left, right)
        if var:
            self.currentscope.addvar(var)

    def scanconditional(self, ptr):
        left = ptr.childs[0]
        right = ptr.childs[1]
        condition = left.childs[0]
        self.scantypes(ptr, right, condition)
        if len(left.childs) == 2:
            self.subscanconditional(left.childs[1])

    def subscanconditional(self, additional):
        logical_operator = additional.childs[0]
        condition = additional.childs[1]
        self.scantypes(additional, logical_operator, condition)
        if len(additional.childs) == 3:
            self.subscanconditional(additional.childs[2])

    def scan(self, ptr: NodeStruct):
        if ptr.name not in ["ASSIGNMENT", "CONDITIONAL_OPERATOR", "INTERNAL_OPERATOR"]:
            for child in ptr.childs:
                self.scan(child)
        elif ptr.name == "ASSIGNMENT":
            self.scanassignment(ptr)
        elif ptr.name == "CONDITIONAL_OPERATOR":
            self.scanconditional(ptr)
            newscope = self.currentscope.newscope()
            self.currentscope = newscope
            self.scan(ptr.childs[2])
            self.currentscope = self.currentscope.prev
            if len(ptr.childs) == 7:
                newscope = self.currentscope.newscope()
                self.currentscope = newscope
                self.scan(ptr.childs[6])
                self.currentscope = self.currentscope.prev
        elif ptr.name == "INTERNAL_OPERATOR":
            if ptr.childs[0].name == "T":
                if len(ptr.childs[0].childs) != self.currentscope.level:
                    sys.stderr.write('Wrong tabulation')
                    sys.exit(1)
                for inners in ptr.childs:
                    self.scan(inners)
            else:
                sys.stderr.write('No tabulation')
                sys.exit(1)

    def scanexpression(self, ptr):
        if ptr.childs[1].name == "VARIABLE":
            if not self.checkvarbool(ptr.childs[1], self.rootscope):
                sys.stderr.write('Unresolved variable: %s\n' % ptr.childs[1].value)
                sys.exit(1)
            elif self.checkvar(ptr.childs[1], self.rootscope)[1] == "STRING":
                sys.stderr.write('Expected type \'SupportsFloat\': %s\n' % ptr.childs[0].name)
                sys.exit(1)
            elif ptr.childs[1] == "OPERATION":
                self.subscantypes(ptr.childs[1])
                self.scanexpression(ptr)
        return True

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
            if self.checkvarbool(left, self.rootscope):
                var = self.checkvar(left, self.rootscope)
                if (var[1], right.name) in self.illegalcombination:
                    sys.stderr.write('Illegal type: %s\n' % right.name)
                    sys.exit(1)
                elif right.name == "VARIABLE":
                    if self.checkvarbool(right, self.rootscope):
                        var2 = self.checkvar(right, self.rootscope)
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
        elif left.name == "EXPRESSION":
            if self.scanexpression(left):
                if ("FLOAT", right.name) in self.illegalcombination:
                    sys.stderr.write('Illegal type: %s\n' % right.name)
                    sys.exit(1)
                else:
                    operation.name = "FLOAT"
        elif right.name == "VARIABLE":
            if self.checkvarbool(right, self.rootscope):
                var = self.checkvar(right, self.rootscope)
                if (var[1], left.name) in self.illegalcombination:
                    sys.stderr.write('Illegal type: %s\n' % right.name)
                    sys.exit(1)
                elif (var[1], left.name) not in self.illegalcombination:
                    operation.name = var[1]
            else:
                sys.stderr.write('Unresolved variable: %s\n' % left.value)
                sys.exit(1)
        elif right.name == "EXPRESSION":
            if self.scanexpression(left):
                if ("FLOAT", right.name) in self.illegalcombination:
                    sys.stderr.write('Illegal type: %s\n' % right.name)
                    sys.exit(1)
                else:
                    operation.name = "FLOAT"
        elif (left.name, right.name) not in self.illegalcombination:
            operation.name = left.name

