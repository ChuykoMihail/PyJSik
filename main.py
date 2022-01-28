import math

import lexer.lexicalAnalizer as la
import IOpackage.ReadWriteClass as IO
from syntaxer.syntaxanalizer import SyntaxAnalizer
from syntaxer.sintaxunit import SyntaxUnit
from syntaxer.rule import Rule
from syntaxer.grammar import Grammar
from syntaxer.ATS import SyntacticalTree
from semanticaltree.operationtree import SyntacticsStructure
from semanticaltree.semanticalanalizer import SemanticalAnalyzer
from codegenerator.codegenerator import CodeGenerator
from test.RunTests import Tester
from pathlib import Path

def test():
    sa = SyntaxAnalizer()
    code = IO.read()
    tokens = la.parse(code)
    print(la.lextableToString(tokens.tokens_array))
    table = sa.earley(rule=sa.grammatic.PROGRAMM, text=la.lextableToString(tokens.tokens_array))
    parsed = sa.right_parsing(table)
    tree = SyntacticalTree(parsed)
    tree.printTree()
    IO.writeSyntaxTree(tree)
    operationtree = SyntacticsStructure(tree)
    operationtree.printast()
    IO.writeOperationTree(operationtree)
    sema = SemanticalAnalyzer(operationtree)
    translator = CodeGenerator(operationtree, sema.variables)
    translator.translate(operationtree.root)
    print(translator.output)
    IO.writeCode(translator.output)

if __name__ == '__main__':
    test()
    math.sqrt("sdf")





