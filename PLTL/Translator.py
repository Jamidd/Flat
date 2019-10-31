from Parser import MyParser
import os


class Translator:
    def __init__(self):
        self.reserved = {"true", "false", "~", "Y", "S", "&", "|"}

    def __call__(self, f):
        parser = MyParser()
        parsed_formula = parser(f)
        return self.trans_fol(parsed_formula)

    def get_alphabet(self, formula):
        if type(formula) == str:
            if formula not in self.reserved:
                return set([formula])
            return set([])
        else:
            if formula[0] not in self.reserved:
                return formula[0]
            else:
                if len(formula) == 3:
                    return self.get_alphabet(formula[1]).union(self.get_alphabet(formula[2]))
                else:
                    return self.get_alphabet(formula[1])

    def alphabet_no_comma(self, formula):
        res = ""
        P = list(self.get_alphabet(formula))
        if len(P) != 0:
            it = P[0]
            res += it.upper()
            for it in P[1:]:
                res += ", " + it.upper()
        return res

    def trans_fol(self, formula):
        res = ""

        P = self.alphabet_no_comma(formula)
        if len(P) > 0:
            res = "m2l-str;\n"
            res += f"var2 {P};\n"
        res += self.sub_trans_fol(formula)
        return f"{res};\n"

    def sub_trans_fol(self, formula, t=0):
        if len(formula) == 0:
            return ""
        res = ""
        if formula[0] == "~":
            res = "~("
            res += self.sub_trans_fol(formula[1], t)
            res += ")"

        elif formula[0] == "Y":
            exs = "x" + str(t + 1)
            res = '(ex1 ' + exs + ': ' + exs + ' = '
            if t == 0:
                res += 'max($) - 1 & max($) > 0 & ('
            else:
                ts = "x" + str(t)
                res += ts + ' - 1 & ' + exs + ' > 0 & '
            res += self.sub_trans_fol(formula[1], t + 1)
            res += "))"

        elif formula[0] == "S":
            exs = "x" + str(t + 1)
            alls = "x" + str(t + 2)
            if t == 0:
                ts = 'max($)'
            else:
                ts = "x" + str(t)

            res = '(ex1 ' + exs + ': 0 <= ' + exs + ' & ' + exs + ' <= ' + ts + ' & ('
            res += self.sub_trans_fol(formula[2], t + 1)
            res += ') & (all1 ' + alls + ': ' + exs + ' < ' + alls + ' & ' + alls + ' <= ' + ts + ' => ('
            res += self.sub_trans_fol(formula[1], t + 2)
            res += ')))'

        elif formula[0] == "|":
            res += "((" 
            res += self.sub_trans_fol(formula[1], t)
            res += ") | ("
            res += self.sub_trans_fol(formula[2], t) 
            res += "))"

        elif formula[0] == "&":
            res += "((" 
            res += self.sub_trans_fol(formula[1], t)
            res += ") & ("
            res += self.sub_trans_fol(formula[2], t) 
            res += "))"

        elif formula == "true":
            res += "(true)"

        elif formula == "false":
            res += "(false)"
            
        else:
            if t == 0:
                ts = "(" + str(t)
            else:
                ts = "(x" + str(t)
            res += ts + " in "
            res += self.alphabet_no_comma(formula)
            res += ")"
        return res

    def get_edge(self, t, v):
        def get_label(av):
            if av[0] == "X":
                return ""
            elif av[0] == "1":
                return f"{av[1]}"
            elif av[0] == "0":
                return f"!{av[1]}"
        s1 = t[:t.index(': ')].replace('State ', 'S')
        s2 = t[t.index(' -> ')+4:].replace('state ', 'S')
        label = list(filter(lambda x: x != "", map(get_label, zip(list(t[t.index(': ')+2: t.index(' -> ')]), v))))
        return (s1, s2, label)

    def read_dfa(self, f):
        # revisar bien el output de mona
        text = []
        with open(f, "r") as file:
            text = file.read().strip().split('\n')

        variables = text.pop(0)[len("DFA for formula with free variables: "):-1].split(' ')
        initial_state = f"""S{text.pop(0)[len("Initial state: ")]}"""
        acepting_states = set(list(map(lambda x: f"""S{x}""", text.pop(0)[len("Accepting states: "):-1].split(' '))))
        while "Transitions" not in text[0]:
            text.pop(0)
        text.pop(0)
        edges = dict()
        states = set()
        while text:
            if "State" not in text[0]:
                break
            s1, s2, label = self.get_edge(text.pop(0), variables)
            states.add(s1)
            states.add(s2)
            edges[(s1, "&".join(label).lower())] = s2

        return {"alphabet": set(variables), "states": states , "initial_state": initial_state, "accepting_states": acepting_states, "transitions": edges}

    def pass_trough_mona(self, formula, quiet = False):
        parser = MyParser()
        parsed_formula = parser(formula)
        if not quiet:
            print(parsed_formula)
        formula = self.trans_fol(parsed_formula)

        try:
            with open("formula.mona", "w") as file:
                file.write(formula)
        except IOError:
            print("IOError pass_trough_mona")
            return
        try:
            os.system("mona -u -w -q formula.mona > dfa.txt")
        except:
            print("Mona error")
            return