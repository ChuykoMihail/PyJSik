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

class Tester:
    def __init__(self):
        self.run()

    def test(self, number):
        sa = SyntaxAnalizer()
        code = IO.read("Test "+str(number))
        tokens = la.parse(code)
        print(la.lextableToString(tokens.tokens_array))
        table = sa.earley(rule=sa.grammatic.PROGRAMM, text=la.lextableToString(tokens.tokens_array))
        parsed = sa.right_parsing(table)
        tree = SyntacticalTree(parsed)
        tree.printTree()
        IO.writeSyntaxTree(tree, "Test "+ str(number))
        operationtree = SyntacticsStructure(tree)
        operationtree.printast()
        IO.writeOperationTree(operationtree, "Test "+str(number))
        sema = SemanticalAnalyzer(operationtree)
        translator = CodeGenerator(operationtree, sema.variables)
        translator.translate(operationtree.root)
        print(translator.output)
        IO.writeCode(translator.output, "Test "+str(number))

    def run(self):
        for i in range(2):
            self.test(i)

