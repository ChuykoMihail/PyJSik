from semanticaltree.semanticalanalizer import SyntacticsStructure
from semanticaltree.semanticalanalizer import NodeStruct
from semanticaltree.semanticalanalizer import Scope


class CodeGenerator:
    def __init__(self, tree, scope: Scope, maxlevel):
        self.tree: SyntacticsStructure = tree
        self.root: NodeStruct = self.tree.root
        self.rootscope = scope
        self.currentscope = self.rootscope
        self.output = ""
        self.logicbinoperation = ["and", "or"]
        self.unaroperation = ["not"]
        self.binaroperator = ["+", "-", "*", "/", ">", "<","<=",">=", "==", "!="]
        self.scopecount = 0
        self.currlevel = 0
        self.maxlevel = maxlevel
        self.levels = [0 for element in range(maxlevel+1)]

    def translate(self, ptr):
        self.output+=self.vardeclaration()
        if self.root.name == "COMPOUND_OPERATOR":
            self.output+=self.translatesingle(self.root.childs[0])
        else:
            self.output += self.translateall(ptr)

    def translateall(self, ptr):
        localoutput = ""
        for child in ptr.childs:
            if child.name == "COMPOUND_OPERATOR":
                localoutput += self.translatesingle(child.childs[0])
            elif child.name == "PROGRAMM":
                localoutput += self.translateall(child)
        return localoutput

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


    # def translateinner(self, inner):
    #     localoutput = ""
    #     localoutput += "\t"*len(inner.childs[0].childs)
    #     localoutput += self.translatesingle(inner.childs[1].childs[0])
    #     if len(inner.childs) == 4:
    #         localoutput += self.translateinner(inner.childs[3])
    #     return localoutput

    def translatesingle(self, compound: NodeStruct):
        localoutput = ""
        if compound.name == "ASSIGNMENT":
            localoutput += compound.childs[0].value + " = "
            localoutput += self.translateexpression(compound.childs[1])
        elif compound.name == "CONDITIONAL_OPERATOR":
            level = self.currentscope.level+1
            buaty = "\t"*(level)
            if len(compound.childs) <= 4:
                self.currentscope = self.currentscope.subscope[self.levels[level]]
                self.levels[level]+=1
                localoutput += "if ("
                localoutput += self.translatelogicalexpression(compound.childs[0]) + ") { \n"
                localoutput += buaty+self.vardeclaration()
                if compound.childs[2].name == "COMPOUND_OPERATOR":
                    localoutput += buaty+self.translatesingle(compound.childs[2].childs[0]) + "\t"*(level-1)+"}"
                elif compound.childs[2].name == "PROGRAMM":
                    localoutput += buaty+self.translateall(compound.childs[2]) + "\t"*(level-1)+"}"
                self.currentscope = self.currentscope.prev
                if self.maxlevel-self.currentscope.level >1:
                    for i in range(self.currentscope.level+2, self.maxlevel+1):
                        self.levels[i] = 0
            elif len(compound.childs) <= 8:
                self.currentscope = self.currentscope.subscope[self.levels[level]]
                self.levels[level] += 1
                localoutput += "if ("
                localoutput += self.translatelogicalexpression(compound.childs[0]) + ") { \n"
                localoutput += buaty+self.vardeclaration()
                if compound.childs[2].name == "COMPOUND_OPERATOR":
                    localoutput += buaty+self.translatesingle(compound.childs[2].childs[0]) + "\t"*(level-1)+"}"
                elif compound.childs[2].name == "PROGRAMM":
                    localoutput += buaty+self.translateall(compound.childs[2]) + "\t"*(level-1)+"}"
                localoutput += "else {\n"
                # self.currentscope = self.currentscope.prev.subscope[self.levels[level]]
                self.currentscope = self.currentscope.prev
                if self.maxlevel-self.currentscope.level >1:
                    for i in range(self.currentscope.level+2, self.maxlevel+1):
                        self.levels[i] = 0
                self.currentscope = self.currentscope.subscope[self.levels[level]]
                self.levels[level] += 1
                localoutput += buaty + self.vardeclaration()
                if compound.childs[6].name == "COMPOUND_OPERATOR":
                    localoutput += buaty+self.translatesingle(compound.childs[6].childs[0]) + "\t"*(level-1)+"}"
                elif compound.childs[6].name == "PROGRAMM":
                    localoutput += buaty+self.translateall(compound.childs[6]) + "\t"*(level-1)+"}"
                self.currentscope = self.currentscope.prev
                if self.maxlevel-self.currentscope.level >1:
                    for i in range(self.currentscope.level+2, self.maxlevel+1):
                        self.levels[i] = 0
        elif compound.name == "WHILE":
            level = self.currentscope.level + 1
            buaty = "\t" * (level)
            self.currentscope = self.currentscope.subscope[self.levels[level]]
            self.levels[level] += 1
            localoutput += "while ("
            localoutput += self.translatelogicalexpression(compound.childs[0]) + ") { \n"
            localoutput += buaty+self.vardeclaration()
            if compound.childs[2].name == "COMPOUND_OPERATOR":
                localoutput += buaty + self.translatesingle(compound.childs[2].childs[0]) + "\t" * (level - 1) + "}"
            elif compound.childs[2].name == "PROGRAMM":
                localoutput += buaty + self.translateall(compound.childs[2]) + "\t" * (level - 1) + "}"
            if len(compound.childs) > 4:
                localoutput += "else {\n"
                self.currentscope = self.currentscope.prev
                if self.maxlevel - self.currentscope.level > 1:
                    for i in range(self.currentscope.level + 2, self.maxlevel + 1):
                        self.levels[i] = 0
                self.currentscope = self.currentscope.subscope[self.levels[level]]
                self.levels[level] += 1
                localoutput += buaty+self.vardeclaration()
                if compound.childs[6].name == "COMPOUND_OPERATOR":
                    localoutput += buaty + self.translatesingle(compound.childs[6].childs[0]) + "\t" * (level - 1) + "}"
                elif compound.childs[6].name == "PROGRAMM":
                    localoutput += buaty + self.translateall(compound.childs[6]) + "\t" * (level - 1) + "}"
            self.currentscope = self.currentscope.prev
            if self.maxlevel - self.currentscope.level > 1:
                for i in range(self.currentscope.level + 2, self.maxlevel + 1):
                    self.levels[i] = 0
        elif compound.name == "PRINT":
            localoutput += "console.log("
            localoutput += self.translateexpression(compound.childs[0])+")"
        localoutput += "\n"
        return localoutput
