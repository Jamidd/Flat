from Translator import Translator
from PySimpleAutomata import DFA, automata_IO


formula = "(a|b)*.a.b.b.c"#"(cafe|te)*.cuenta.salir"#"a|b.c|d.e"#"""a|b.c*"#"(a|b)*.a.b.b.#"
formula = f'({formula}).#'
trans = Translator()
"""
def get_dfa(formula, act_dict):
    first_pos = {}
    last_pos = {}
    follow_pos = {}
    nullable = {}
    element = {}
    dfa = {}

    def init_first_last_pos():

        i = 1
        for name in act_dict.keys():
            if name != 'ϵ':
                first_pos[name] = set([i])
                last_pos[name] = set([i])
                element[i] = act_dict[name]
                if act_dict[name] == '#':
                    end_num = i
                follow_pos[i] = set([])
                i += 1
            else:
                first_pos[name] = set([])
                last_pos[name] = set([])

        return  end_num

    def set_first_last_pos(formula):

        if formula == None:
            return set([]), set([])

        if type(formula) == tuple:
            if len(formula) == 2:
                operator, c1 = formula
                c2 = None

            elif len(formula) == 3:
                operator, c1, c2 = formula

            set_first_last_pos(c1)
            set_first_last_pos(c2)

            if operator == '*':
                nullable[formula] = True

                first_pos[formula] = first_pos[c1]
                last_pos[formula] = last_pos[c1]

            elif operator == '|':
                nullable[formula] = nullable[c1] or nullable[c2]

                first_pos[formula] = first_pos[c1].union(first_pos[c2])
                last_pos[formula] = last_pos[c1].union(last_pos[c2])

            elif operator == '.':
                nullable[formula] = nullable[c1] and nullable[c2]

                if nullable[c1]:
                    first_pos[formula] = first_pos[c1].union(first_pos[c2])
                else:
                    first_pos[formula] = first_pos[c1]

                if nullable[c2]:
                    last_pos[formula] = last_pos[c1].union(last_pos[c2])
                else:
                    last_pos[formula] = last_pos[c2]

        else:
            if formula == 'ϵ':
                nullable[formula] = True
            else:
                nullable[formula] = False

    def set_follow_pos(formula):

        if type(formula) == tuple:
            if len(formula) == 2:
                operator, c1 = formula
                c2 = None

            elif len(formula) == 3:
                operator, c1, c2 = formula

            set_follow_pos(c1)
            set_follow_pos(c2)

            if operator == '.':
                for i in last_pos[c1]:
                    follow_pos[i] = follow_pos[i].union(first_pos[c2])

            elif operator == '*':
                for i in last_pos[formula]:
                    follow_pos[i] = follow_pos[i].union(first_pos[formula])
        else:
            return

    def set_dfa():

        simbols = set(act_dict.values())
        simbols.discard('#')

        nodes = [tuple(sorted(list(first_pos[formula])))]
        for node in nodes:
            edges = {}
            for arc in simbols:
                next = set([])
                for i in node:
                    if element[i] == arc:
                        next = next.union(follow_pos[i])
                edges[arc] = tuple(sorted(list(next)))
            dfa[tuple(sorted(list(node)))] = edges

            for n in edges.values():
                n = tuple(sorted(list(n)))
                if n not in dfa:
                    nodes.append(n)

    def prettify_dfa(end_num):

        new_nodes = {}
        full_dfa = {}
        goals = set([])
        i = 1
        for node in dfa:
            if node not in new_nodes:
                new_nodes[node] = i
                i += 1
            new_edges = {}
            for edge in dfa[node]:
                if dfa[node][edge] not in new_nodes:
                    new_nodes[dfa[node][edge]] = i
                    i += 1
                new_edges[edge] = new_nodes[dfa[node][edge]]
            full_dfa[new_nodes[node]] = new_edges

            if end_num in node:
                goals.add(new_nodes[node])

        return full_dfa, goals

    end_num = init_first_last_pos()
    set_first_last_pos(formula)
    set_follow_pos(formula)
    set_dfa()
    dfa, goals = prettify_dfa(end_num)
    return dfa, goals
"""
trans.pass_trough_mona(formula)
dfa = trans.read_dfa('dfa.txt')


automata_IO.dfa_to_dot(dfa, 'eliminar.dfa', './')

