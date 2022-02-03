from .state import State
from .grammar import Grammar
from .rule import Rule
from .sintaxunit import SyntaxUnit
from .column import Column


class SyntaxAnalizer:

    def __init__(self):
        self.grammatic = Grammar()

    def predict(self, col, rule):
        for prod in rule.productions:
            col.add(State(rule.name, prod, 0, col))

    def scan(self, col, state, token):
        if token != col.token:
            return
        if state.name == self.grammatic.GAMMA_RULE:
            print("Gamma")
        col.add(State(state.name, state.production, state.dot_index + 1, state.start_column))

    def complete(self, col, state):
        if not state.completed():
            return
        for st in state.start_column:
            term = st.next_term()
            if not isinstance(term, Rule):
                continue
            if term.name == state.name:
                col.add(State(st.name, st.production, st.dot_index + 1, st.start_column))

    def earley(self, rule, text):
        table = [Column(i, tok) for i, tok in enumerate([None] + text.split())]
        table[0].add(State(self.grammatic.GAMMA_RULE, SyntaxUnit(rule), 0, table[0]))

        for i, col in enumerate(table):
            for state in col:
                if state.completed():
                    self.complete(col, state)
                else:
                    indextoken = i
                    term = state.next_term()
                    if isinstance(term, Rule):
                        self.predict(col, term)
                    elif i + 1 < len(table):
                        self.scan(table[i + 1], state, term)
        for st in table[-1]:
            if st.name == self.grammatic.GAMMA_RULE and st.completed():
                return table
        else:
            raise ValueError(
                "SyntaxError \'{} {}\':invalid syntax, Expected:{}".format(table[indextoken].token,
                                                                           table[indextoken + 1].token, term))

    def right_parsing(self, table):
        state = None
        for st in table[-1]:
            if st.name == self.grammatic.GAMMA_RULE and st.completed():
                state = st
        return self.sub_parsing([], table, state, state.end_column.index)

    def sub_parsing(self, acc, table, state: State, j: int):
        acc.append(Rule(state.name, state.production))
        k = len(state.production) - 1
        c = j
        while k >= 0:
            Xk = state.production[k]
            if not isinstance(Xk, Rule):
                k -= 1
                c -= 1
            else:
                Ic = table[c]
                # founding the state for Nonterminal Xk
                searchstate = None
                searchflag = False
                for st in Ic:
                    if searchflag:
                        break
                    if st.completed() and st.name == Xk.name:
                        r = st.start_column.index
                        Ir = table[r]
                        # founding the previous state of Nonterminal Xk
                        for prevst in Ir:
                            if state.production == prevst.production and prevst.dot_index == k and state.name == prevst.name \
                                    and state.start_column == prevst.start_column:
                                searchstate = st
                                searchflag = True
                                break
                self.sub_parsing(acc, table, searchstate, c)
                k -= 1
                c = r
        return acc
