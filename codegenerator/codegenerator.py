from semanticaltree.semanticalanalizer import SyntacticsStructure
from semanticaltree.semanticalanalizer import NodeStruct

class CodeGenerator:
    def __init__(self, tree, variables):
        self.tree: SyntacticsStructure = tree
        self.root: NodeStruct = self.tree.root
        self.variables = variables
        self.output = ""
        self.binaroperator = ["+", "-", "*", "/"]

    def translate(self, ptr):
        self.vardeclaration()
        if self.root.name == "COMPOUND_OPERATOR":
            self.translatesingle(self.root.childs[0])
        else:
            self.translateall(ptr)


    def translateall(self, ptr):
        for child in ptr.childs:
            if child.name == "COMPOUND_OPERATOR":
                self.translatesingle(child.childs[0])
            elif child.name == "PROGRAMM":
                self.translateall(child)

    def vardeclaration(self):
        if len(self.variables) > 0:
            self.output += "let "
            if len(self.variables) == 1:
                self.output += self.variables[0][0]
                self.output += ";\n"
            else:
                for var in self.variables:
                    self.output += var[0] + ", "
                self.output = self.output[:len(self.output)-2]
                self.output += ";\n"

    def translateexpression(self, ptr: NodeStruct):
        localoutput = ""
        if ptr.value in self.binaroperator:
            localoutput += self.translateexpression(ptr.childs[0])
            localoutput += ptr.value
            localoutput += self.translateexpression(ptr.childs[1])
            localoutput = "("+localoutput+")"
            return localoutput
        elif ptr.name in ["INTEGER", "BOOL", "VARIABLE"]:
            localoutput += str(ptr.value)
            return localoutput

    def translatesingle(self, compound: NodeStruct):
        if compound.name == "ASSIGNMENT":
            self.output += compound.childs[0].value + " = "
            self.output += self.translateexpression(compound.childs[1])
        self.output += "\n"


