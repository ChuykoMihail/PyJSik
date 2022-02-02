from syntaxer.rule import Rule
from pathlib import Path

currpath = Path().cwd().resolve()
currpath = str(currpath)+"\\test\\"
def read(path=""):
    if path == "":
        with open('input.txt', 'r') as f:
            inputCode = f.read()
    else:

        with open(currpath+path+"\\input.txt", 'r') as f:
            inputCode = f.read()
    inputCode = inputCode.replace("\n", "\\n")
    inputCode = inputCode.replace("    ", "\\t")
    inputCode = inputCode.replace(" ", "")
    return inputCode


def writeCode(outputCode, path=""):
    if path == "":
        with open('output.txt', 'w') as f:
            f.write(outputCode)
    else:
        with open(currpath+ path+'\\output.txt', 'w') as f:
            f.write(outputCode)

def writeSyntaxTree(tree, path = ""):
    def search(ptr, level, file):
        if ptr.prev is None:
            l = 0
        else:
            if isinstance(ptr.prev.left, Rule):
                l = len(ptr.prev.left.name)
            else:
                l = len(ptr.prev.left)
        file.write(str(level) + ':' + '|' + level * ' ' + '├-' + str(ptr.left) + "\n")
        if ptr.childs:
            for i in ptr.childs:
                search(i, level + 1, file)

    if path == "":
        file = open("outputSyntaxTree.txt", 'w', encoding="utf-8")
        level = 0
        search(tree.root, level, file)
    else:
        with open(currpath+path+"\\outputSyntaxTree.txt", 'w', encoding="utf-8") as file:
            level = 0
            search(tree.root, level, file)

def writeOperationTree(tree, path=""):
    def search(ptr, level, file):
        file.write(str(level) + ':' + '|' + level * '+' + '├-' + str(ptr) + "\n")
        if ptr.childs:
            for i in ptr.childs:
                search(i, level + 1, file)
    if path == "":
        file = file = open("outputOperationTree.txt", 'w', encoding="utf-8")
        level = 0
        search(tree.root, level, file)
    else:
        with open(currpath+path+"\\outputOperationTree.txt", 'w', encoding="utf-8") as file:
            level = 0
            search(tree.root, level, file)
