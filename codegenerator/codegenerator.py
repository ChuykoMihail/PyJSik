from semanticaltree.semanticalanalizer import SyntacticsStructure
from semanticaltree.semanticalanalizer import NodeStruct
from semanticaltree.semanticalanalizer import Scope


class CodeGenerator:
    def __init__(self, tree, scope: Scope):
        self.tree: SyntacticsStructure = tree
        self.root: NodeStruct = self.tree.root
        self.rootscope = scope
        self.currentscope = self.rootscope
        self.output = ""
        self.logicbinoperation = ["and", "or"]
        self.unaroperation = ["not"]
        self.binaroperator = ["+", "-", "*", "/", ">", "<","<=",">=", "==", "!="]

    def translate(self, ptr):
        self.output+=self.vardeclaration()
        if self.root.name == "COMPOUND_OPERATOR":
            self.output+=self.translatesingle(self.root.childs[0])
        else:
            self.translateall(ptr)

    def translateall(self, ptr):
        for child in ptr.childs:
            if child.name == "COMPOUND_OPERATOR":
                self.output+=self.translatesingle(child.childs[0])
            elif child.name == "PROGRAMM":
                self.translateall(child)

    def vardeclaration(self):
        localoutput = ""
        if len(self.currentscope.variables) > 0:
            localoutput += "let "
            if len(self.currentscope.variables) == 1:
                localoutput += self.currentscope.variables[0][0]
                localoutput += ";\n"
                # return localoutput
            else:
                for var in self.currentscope.variables:
                    localoutput += var[0] + ", "
                localoutput = localoutput[:len(localoutput) - 2]
                localoutput += ";\n"
                # return localoutput
        return localoutput

    def translateexpression(self, ptr: NodeStruct):
        localoutput = ""
        if ptr.value in self.binaroperator:
            localoutput += self.translateexpression(ptr.childs[0])
            localoutput += ptr.value
            localoutput += self.translateexpression(ptr.childs[1])
            localoutput = localoutput
            return localoutput
        elif ptr.name in ["INTEGER", "BOOL", "VARIABLE", "REAL_NUMBER", "FLOAT"]:
            localoutput += str(ptr.value)
            return localoutput
        elif ptr.name in ["STRING"]:
            localoutput += "\"" + ptr.value + "\""
            return localoutput
        elif ptr.name in ["EXPRESSION"]:
            if ptr.childs[0].name != "abs":
                ptr.childs[0].name = ptr.childs[0].name.replace("m", "M")
            else:
                ptr.childs[0].name = "Math."+ptr.childs[0].name
            localoutput += ptr.childs[0].name + "("
            localoutput += self.translateexpression(ptr.childs[1])
            localoutput += ")"
            return localoutput
        # elif ptr.name == "FLOAT":
        #     localoutput+=ptr.childs[0].value+ptr.childs[1].value
        #     return localoutput

    def translatelogicalexpression(self, condition):
        localoutput = ""
        if len(condition.childs) == 1:
            localoutput += self.translateexpression(condition.childs[0])
        else:
            localoutput += self.translateexpression(condition.childs[0])
            localoutput += self.translateadditional(condition.childs[1])
        return localoutput

    def translateadditional(self, addition):
        localoutput = ""
        logicaloperator = addition.childs[0].value
        if logicaloperator == "and":
            localoutput += " && "
        else:
            localoutput += " || "
        localoutput += self.translateexpression(addition.childs[1])
        if len(addition.childs) == 3:
            localoutput += self.translateadditional(addition.childs[2])
        return localoutput


    def translateinner(self, inner):
        localoutput = ""
        localoutput += "\t"*len(inner.childs[0].childs)
        localoutput += self.translatesingle(inner.childs[1].childs[0])
        if len(inner.childs) == 4:
            localoutput += self.translateinner(inner.childs[3])
        return localoutput

    # def translatesingle(self, compound: NodeStruct):
    #     localoutput = ""
    #     if compound.name == "ASSIGNMENT":
    #         self.output += compound.childs[0].value + " = "
    #         self.output += self.translateexpression(compound.childs[1])
    #     elif compound.name == "CONDITIONAL_OPERATOR":
    #         self.output += "if ("
    #         self.output += self.translatelogicalexpression(compound.childs[0]) + ") { \n"
    #         self.output += self.translateinner(compound.childs[2])
    #     self.output += "\n"

    def translatesingle(self, compound: NodeStruct):
        localoutput = ""
        if compound.name == "ASSIGNMENT":
            localoutput += compound.childs[0].value + " = "
            localoutput += self.translateexpression(compound.childs[1])
        elif compound.name == "CONDITIONAL_OPERATOR":
            if len(compound.childs) <= 4:
                self.currentscope = self.currentscope.subscope[0]
                localoutput += "if ("
                localoutput += self.translatelogicalexpression(compound.childs[0]) + ") { \n"
                localoutput += (len(compound.childs[2].childs[0].childs))*"\t"+self.vardeclaration()
                localoutput += self.translateinner(compound.childs[2]) + (
                        len(compound.childs[2].childs[0].childs)-1)*"\t" + "}"
            elif len(compound.childs) <= 8:
                self.currentscope = self.currentscope.subscope[0]
                localoutput += "if ("
                localoutput += self.translatelogicalexpression(compound.childs[0]) + ") { \n"
                localoutput += (len(compound.childs[2].childs[0].childs)) * "\t" + self.vardeclaration()
                localoutput += self.translateinner(compound.childs[2]) + (
                        len(compound.childs[2].childs[0].childs) - 1) * "\t" + "} "+"else {\n"
                self.currentscope = self.currentscope.prev.subscope[1]
                localoutput += (len(compound.childs[2].childs[0].childs)) * "\t" + self.vardeclaration()
                localoutput += self.translateinner(compound.childs[6]) + (
                        len(compound.childs[2].childs[0].childs) - 1) * "\t" + "}"
        elif compound.name == "WHILE":
            self.currentscope = self.currentscope.subscope[0]
            localoutput+="while ("
            localoutput += self.translatelogicalexpression(compound.childs[0]) + ") { \n"
            localoutput += (len(compound.childs[2].childs[0].childs)) * "\t" + self.vardeclaration()
            localoutput += self.translateinner(compound.childs[2]) + (
                    len(compound.childs[2].childs[0].childs) - 1) * "\t" + "}"




        localoutput += "\n"
        return localoutput
