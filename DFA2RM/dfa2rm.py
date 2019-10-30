from collections import defaultdict
from functools import reduce
from dd.autoref import BDD
import itertools
from PySimpleAutomata import DFA
from PySimpleAutomata import automata_IO as AutIO


def read_formula(file):
    f = []
    r = []
    with open(file, "r") as file:
        for _ in range(int(file.readline())):
            f.append(file.readline().strip())
            r.append(int(file.readline().strip()))
    return f, r


def get_new_state():
    counter = 0
    while 1:
        yield f"""S{counter}"""
        counter += 1


def add_reward(automata, n):
    r = dict()
    for ste in automata['accepting_states']:
        r[ste] = n
    automata['reward'] = r
    return automata


def set_in_out(automata):
    set_in = defaultdict(list)
    set_out = defaultdict(list)
    for ini, lbl in automata["transitions"]:
        end = automata["transitions"][(ini, lbl)]
        if lbl == "": lbl = "TRUE"
        set_in[end].append((ini, lbl))
        set_out[ini].append((end, lbl))
    automata["in"] = set_in
    automata["out"] = set_out
    return automata


def bdd_to_formula(bdd, bd):
    bd = list(bdd.pick_iter(bd))[0]
    simbol = {"True": "", "False": "!"}
    return "&".join([f"{simbol[str(bd[k])]}{k}" for k in bd])#.lower()


def dfa_intersection_to_rm(automata, minimize=False):  # from alberto and https://spot.lrde.epita.fr/ipynb/product.html
    result = {
        'alphabet': set().union(*[x["alphabet"] for x in automata]),
        'states': set(),
        'initial_state': "",
        'accepting_states': set(),
        'transitions': dict(),
        'reward': defaultdict(int)
    }

    sdict = {}
    todo = []

    new_state = get_new_state()

    def dst(state_numbers):
        state_numbers_tuple = tuple(state_numbers)
        p = sdict.get(state_numbers_tuple)
        if p is None:
            p = next(new_state)
            sdict[state_numbers_tuple] = p
            todo.append((state_numbers_tuple, p))
        return p

    result["initial_state"] = dst([aut['initial_state'] for aut in automata])
    bdd = BDD()
    bdd.declare(*result["alphabet"])

    while todo:
        tuple_rc, osrc = todo.pop()
        lists_of_transitions = [automata[i]['out'][tuple_rc[i]] for i in range(len(automata))]
        for elements in itertools.product(*lists_of_transitions):
            cond = bdd.add_expr("TRUE")
            for ste, edge_cond in elements:
                cond = cond & bdd.add_expr(edge_cond.upper())

            if bdd.to_expr(cond) != "FALSE":
                reward = sum([automata[i]["reward"][elements[i][0]] for i in range(len(elements)) if elements[i][0] in automata[i]['reward']])
                dest = dst([e[0] for e in elements])
                if reward > 0:
                    result["accepting_states"].add(dest)
                result["states"].add(osrc)
                result["states"].add(dest)
                result["reward"][dest] = reward
                result["transitions"][(osrc, bdd_to_formula(bdd, cond))] = dest
    if minimize:
        result = DFA.dfa_co_reachable(result)
    # rename with actual reward
    rm = {
        'alphabet': set(),
        'states': set(),
        'initial_state': "",
        'accepting_states': set(),
        'transitions': dict(),
    }

    rm["alphabet"] = result["alphabet"]

    new_states = dict()
    for k in result["reward"]:
        new_states[k] = f"""{k}\n{"{"}{result["reward"][k]}{"}"}"""
        rm["states"].add(new_states[k])

    if result["initial_state"] not in new_states:
        new_states[result["initial_state"]] = f"""{result["initial_state"]}\n{"{"}0{"}"}"""

    rm["initial_state"] = new_states[result["initial_state"]]  

    new_transitions = dict()
    for ini in result["transitions"]:
        end = result["transitions"][ini]

        ini = (new_states[ini[0]], ini[1])
        end = new_states[end]
        new_transitions[ini] = end

    rm["transitions"] = new_transitions

    return rm


def get_dfas(automata, rewards, reward=False, minimize=False):
    if reward:
        automata = [set_in_out(add_reward(automata[i], rewards[i])) for i in range(len(automata))]
    else:
        automata = [set_in_out(aut) for aut in automata]

    if minimize:
        automata = [DFA.dfa_co_reachable(aut) for aut in automata]

    return automata


def automatas_to_rm(automata, rewards, minimize=False):
    automata = get_dfas(automata, rewards, reward=True, minimize=False)
    return dfa_intersection_to_rm(automata, minimize)
