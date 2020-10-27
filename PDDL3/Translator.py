from Parser import MyParser
import os
from itertools import  product
from PySimpleAutomata import DFA 

class Translator:
    def __init__(self):
        self.reserved = {"true", "false", "~", "&", "|",}
        self.objects = None
        self.formulas = None

    def __call__(self, f):
        parser = MyParser()
        parsed_formula = parser(f)
        if type(parsed_formula) != tuple:
            return ('at-end', parsed_formula)
        return parsed_formula

    def sub_replace(self, formula, k, v):
        formula = list(formula)
        for i, f in enumerate(formula):
            if type(f) == str:
                formula[i] = f.replace(k, v)
            else:
                formula[i] = self.sub_replace(f, k, v)
        return formula if type(formula) == tuple else tuple(formula)

    def replace(self, formula, k, vals):
        options = set()
        for v in vals:
            options = options.union(set(self.sub_replace(formula, k, v)))
        return options

    def get_all_formulas(self, formula):
        new_formulas = set()
        revisar = [formula]

        while len(revisar) > 0 :
            formula = revisar.pop(0)
            if formula[0] == 'and':
                for sub_for in formula[1]:
                    revisar.append(sub_for)

            elif formula[0] == 'forall':
                cambios = {}
                for i in range(0,len(formula[1]), 3):
                    cambios[formula[1][i]] = self.objects[formula[1][i+2]]            
                if set([type(x) for x in formula[2]]) != set([tuple]):
                    formulas = [formula[2]]
                else:
                    formulas = set(formula[2])

                for k in cambios:
                    formulas = self.replace(formulas, k, cambios[k])

                new_formulas = new_formulas.union(formulas)
            else:
                new_formulas = new_formulas.union({formula})
        return new_formulas

    def get_automatas(self, formulas):
        automatas = []
        for formula in formulas:
            if formula[0] == 'at-end':
                a = '_'.join(formula[1]).upper()
                automata = {
                    "alphabet": {a},
                    "states": {'S0', 'S1'},
                    "initial_state": 'S0',
                    "accepting_states": {'S1'},
                    "transitions": {
                        ('S0', f'(!({a}))'): 'S0',
                        ('S0', f'({a})'): 'S1',
                        ('S1', f'({a})'): 'S1',
                        ('S1', f'(!({a}))'): 'S0',
                    }
                }
            elif formula[0] == 'always':
                a = '_'.join(formula[1]).upper()
                automata = {   
                    "alphabet": {a},
                    "states": {'S0', 'S1', 'S2'},
                    "initial_state": 'S0',
                    "accepting_states": {'S1'},
                    "transitions": {
                        ('S0', f'({a})'): 'S1',
                        ('S1', f'({a})'): 'S1',
                        ('S1', f'(!({a}))'): 'S2',
                        ('S0', f'(!({a}))'): 'S2',
                        ('S2', ''): 'S2',
                    }
                }
            elif formula[0] == 'sometime':
                a = '_'.join(formula[1]).upper()
                automata = {   
                    "alphabet": {a},
                    "states": {'S0', 'S1', 'S2'},
                    "initial_state": 'S0',
                    "accepting_states": {'S2'},
                    "transitions": {
                        ('S0', f'(!({a}))'): 'S1',
                        ('S1', f'(!({a}))'): 'S1',
                        ('S1', f'({a})'): 'S2',
                        ('S0', f'({a})'): 'S2',
                        ('S2', ''): 'S2',
                    }
                }
            elif formula[0] == 'within':
                _, t, a = formula
                a = '_'.join(a).upper()
                t = int(float(t))
                alphabet = {str(a)}
                states = set([f'S{x}' for x in range(t+3)])
                initial_states = 'S0'
                accepting_states = {f'S{t+2}'}
                transitions = {}
                for i, j in zip(range(t+1), range(1,t+2)):
                    transitions[(f'S{i}', f'({a})')] = f'S{t+2}'
                    transitions[(f'S{i}', f'(!({a}))')] = f'S{j}'
                
                transitions[(f'S{t+1}', '')] = f'S{t+1}'
                transitions[(f'S{t+2}', '')] = f'S{t+2}'

                automata = {   
                    "alphabet": alphabet,
                    "states": states,
                    "initial_state": initial_states,
                    "accepting_states": accepting_states,
                    "transitions": transitions
                }

            elif formula[0] == 'at-most-once':
                a = '_'.join(formula[1]).upper()
                automata = {   
                    "alphabet": {a},
                    "states": {'S0', 'S1', 'S2', 'S3', 'S4'},
                    "initial_state": 'S0',
                    "accepting_states": {'S1', 'S2', 'S3'},
                    "transitions": {
                        ('S0', f'(!({a}))'): 'S1',
                        ('S1', f'(!({a}))'): 'S1',
                        ('S1', f'({a})'): 'S2',
                        ('S0', f'({a})'): 'S2',
                        ('S2', f'({a})'): 'S2',
                        ('S2', f'(!({a}))'): 'S3',
                        ('S3', f'(!({a}))'): 'S3',
                        ('S3', f'({a})'): 'S4',
                        ('S4', ''): 'S4',
                    }
                }
            elif formula[0] == 'sometime-after':
                _, a, b = formula
                a = '_'.join(a).upper()
                b = '_'.join(b).upper()
                automata = {   
                    "alphabet": {a, b},
                    "states": {'S0', 'S1', 'S2'},
                    "initial_state": 'S0',
                    "accepting_states": {'S1'},
                    "transitions": {
                        ('S0', f'((!({a})) | ({b}))'): 'S1',
                        ('S1', f'((!({a})) | ({b}))'): 'S1',
                        ('S1', f'(({a}) & (!({b})))'): 'S2',
                        ('S2', f'({b})'): 'S1',
                        ('S2', f'(!({b}))'): 'S2',
                        ('S0', f'(({a}) & (!({b})))'): 'S2'
                    }
                }
            elif formula[0] == 'sometime-before':
                _, a, b = formula
                a = '_'.join(a).upper()
                b = '_'.join(b).upper()
                automata = {   
                    "alphabet": {a, b},
                    "states": {'S0', 'S1', 'S2','S3'},
                    "initial_state": 'S0',
                    "accepting_states": {'S1', 'S2'},
                    "transitions": {
                        ('S0', f'((!({b})) & (!({a})))'): 'S1',
                        ('S0', f'(({b}) & (!({a})))'): 'S2',
                        ('S0', f'({a})'): 'S3',
                        ('S1', f'((!({b})) & (!({a})))'): 'S1',
                        ('S1', f'(({b}) & (!({a})))'): 'S2',
                        ('S1', f'({a})'): 'S3',
                        ('S2', ''): 'S2',
                        ('S3', ''): 'S3',
                    }
                }
            elif formula[0] == 'always-within':
                _, t, a, b = formula

                a = '_'.join(a).upper()
                b = '_'.join(b).upper()

                t = int(float(t))
                alphabet = {a, b}
                states = set([f'S{x}' for x in range(t+3)])
                initial_states = 'S0'
                accepting_states = {f'S{t+2}'}
                transitions = {}
                
                transitions[(f'S0', f'(({a}) & (!({b})))')] = f'S1'
                transitions[(f'S0', f'((!({a})) | ({b}))')] = f'S{t+2}'

                for i, j in zip(range(1,t+1), range(2,t+2)):
                    transitions[(f'S{i}', f'(!({b}))')] = f'S{j}'
                    transitions[(f'S{i}', f'({b})')] = f'S{t+2}'
                    transitions[(f'S{t+2}', f'(({a}) & (!({b})))')] = f'S{i}'

                transitions[(f'S{t+1}', '')] = f'S{t+1}'
                transitions[(f'S{t+2}', f'((!({a})) | ({b}))')] = f'S{t+2}'

                automata = {   
                    "alphabet": alphabet,
                    "states": states,
                    "initial_state": initial_states,
                    "accepting_states": accepting_states,
                    "transitions": transitions
                }

            elif formula[0] == 'hold-during':
                _, t1, t2, a = formula
                a = '_'.join(a).upper()
                t1 = int(float(t1))
                t2 = int(float(t2))
                alphabet = {a}
                states = set([f'S{x}' for x in range(t1+t2+3)])
                initial_states = 'S0'
                accepting_states = set([f'S{x}' for x in range(1,t+2)]).union(set([f'S{x}' for x in range(2*t1+1,t1+t2+2)]))
                transitions = {}
                
                for i in range(1,t1):
                    transitions[(f'S{i}', f'({a})')] = f'S{i+1}'
                    transitions[(f'S{i}', f'(!({a}))')] = f'S{t1+1+i}'
                    transitions[(f'S{t1+i}', f'(!({a}))')] = f'S{t1+1+i}'
                    transitions[(f'S{t1+i}', f'({a})')] = f'S{i+1}'

                for i in range(t1, t1+t2+1):
                    transitions[(f'S{i}', f'({a})')] = f'S{i+1}'
                    transitions[(f'S{i}', f'(!({a}))')] = f'S{t1+t2+2}'

                transitions[(f'S{0}', f'({a})')] = f'S{1}'
                transitions[(f'S{0}', f'(!({a}))')] = f'S{t1+1}'

                transitions[(f'S{2*t1}', f'({a})')] = f'S{2*t1+1}'
                transitions[(f'S{2*t1}', f'(!({a}))')] = f'S{t1+t2+2}'

                transitions[(f'S{t1+t2+1}', '')] = f'S{t1+t2+1}'

                transitions[(f'S{t1+t2+2}', '')] = f'S{t1+t2+2}'

                automata = {   
                    "alphabet": alphabet,
                    "states": states,
                    "initial_state": initial_states,
                    "accepting_states": accepting_states,
                    "transitions": transitions
                }

            elif formula[0] == 'hold-after':
                _, t, a = formula
                a = '_'.join(a).upper()
                t = int(float(t))
                alphabet = {a}
                states = set([f'S{x}' for x in range(2*t+5)])
                initial_states = 'S0'
                accepting_states = set([f'S{x}' for x in range(1,t+2)]).union(set([f'S{2*t+3}']))
                transitions = {}

                for i in range(1,t):
                    transitions[(f'S{i}', f'({a})')] = f'S{i+1}'
                    transitions[(f'S{i}', f'(!({a}))')] = f'S{t+2+i}'
                    transitions[(f'S{t+1+i}', f'(!({a}))')] = f'S{t+2+i}'
                    transitions[(f'S{t+1+i}', f'({a})')] = f'S{i+1}'

                transitions[(f'S{0}', f'({a})')] = f'S{1}'
                transitions[(f'S{0}', f'(!({a}))')] = f'S{t+2}'

                transitions[(f'S{t+1}', f'({a})')] = f'S{2*t+3}'
                transitions[(f'S{t+1}', f'(!({a}))')] = f'S{2*t+4}'

                transitions[(f'S{2*t+2}', f'({a})')] = f'S{2*t+3}'
                transitions[(f'S{2*t+2}', f'(!({a}))')] = f'S{2*t+4}'

                transitions[(f'S{2*t+4}', f'({a})')] = f'S{2*t+3}'
                transitions[(f'S{2*t+4}', f'(!({a}))')] = f'S{2*t+4}'

                transitions[(f'S{2*t+3}', '')] = f'S{2*t+3}'

                automata = {   
                    "alphabet": alphabet,
                    "states": states,
                    "initial_state": initial_states,
                    "accepting_states": accepting_states,
                    "transitions": transitions
                }
            else:
                print(1)
                exit()
                # print('unknow formula, check parser', formula)

            automatas.append(automata)
        return automatas

    def translate(self, formula, file_name, num, quiet=False):
        objects, constraints = formula
        self.objects = objects
        parser = MyParser()
        parsed_formula = parser(constraints)            
        if not quiet:
            print(parsed_formula)

        formulas = self.get_all_formulas(parsed_formula)
        automatas = self.get_automatas(formulas)

        return automatas