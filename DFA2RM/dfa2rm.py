from collections import defaultdict
from dd.autoref import BDD
import itertools
from PySimpleAutomata import DFA
from copy import  deepcopy

def read_formula(file):
    f = []
    r = []
    with open(file, "r") as file:
        for _ in range(int(file.readline().strip())):
            line = file.readline().strip()
            while line[0] == '#':
                line = file.readline().strip()
            line += '#'
            f.append(line[:line.index('#')])
            line = file.readline().strip()
            while line[0] == '#':
                line = file.readline().strip()
            line += '#'
            r.append(int(line[:line.index('#')]))
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


def dfa_intersection_to_rm(automata, reduce=False, set_reward=True):  # from alberto and https://spot.lrde.epita.fr/ipynb/product.html
    # TODO consolidar caminos equivalentes
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

    maxima = 0
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
                # TODO: check rm reduce if we want full reduce or to every subgoal
                #if reward > 0:
                #    result["accepting_states"].add(dest)
                if reward > maxima:
                    result["accepting_states"] = set([dest])
                    maxima = reward
                elif reward == maxima:
                    result["accepting_states"].add(dest)

                result["states"].add(osrc)
                result["states"].add(dest)
                # result["reward"][dest] = reward  // This is if you want the reward at the node instead of the edge
                if not set_reward:
                    reward = 0
                result["transitions"][(osrc, bdd_to_formula(bdd, cond))] = (dest, reward) # dest // This is if you want the reward at the node instead of the edge

    if reduce:
        full_transitions = deepcopy(result['transitions'])
        for k in result['transitions']:
            result['transitions'][k] = result['transitions'][k][0] # only the next state
        result = DFA.dfa_co_reachable(result)
        for k in result['transitions']:
            result['transitions'][k] = full_transitions[k]  # return the state and reward
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

    for k in result["states"]: # result["reward"]: // This is if you want the reward at the node instead of the edge
        new_states[k] = f'''{k}''' #  \n{"{"}{result["reward"][k]}{"}"}'''
        rm["states"].add(new_states[k])

    if result["initial_state"] not in new_states:
        new_states[result["initial_state"]] = f"""{result["initial_state"]}\n{"{"}0{"}"}"""

    rm["initial_state"] = new_states[result["initial_state"]]

    new_transitions = dict()
    for ini in result["transitions"]:
        end, reward = result["transitions"][ini]

        #ini = (new_states[ini[0]], ini[1]) // This is if you want the reward at the node instead of the edge
        ini = (new_states[ini[0]], str((ini[1], reward) if reward > 0 else ini[1]))
        end = new_states[end]
        reward = result["reward"][end]
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


def automatas_to_rm(automata, rewards, minimize=False, reward = True):
    automatas = get_dfas(automata, rewards, reward=True, minimize = False)
    return dfa_intersection_to_rm(automatas, minimize, reward)


def add_a(formula):
    reserved = set(['&', '|', '~', '!', '-', '<', '>'])
    cont = False
    ret = ''
    for l in formula:
        if l in reserved:
            cont = False
        elif not cont:
            ret += '@'
            cont = True
        ret += l
    return ret


def write_hoa(dfa, name):
    transByState = defaultdict(list)
    for trans in dfa['transitions']:
        transByState[trans[0]].append((trans[1], dfa['transitions'][trans]))
    hoa = ''
    hoa += 'HOA: v1\n'
    #hoa += 'name: '
    hoa += f'States: {len(dfa["states"])}\n'
    hoa += f'Start: {dfa["initial_state"].replace("S", "")}\n'
    hoa += f'''AP: {len(dfa["alphabet"])} "{'" "'.join(dfa["alphabet"])}"\n'''
    for i, leter in  enumerate(dfa["alphabet"]):
        hoa += f'Alias: @{leter} {i}\n'
    hoa += f'Acceptance: {len(dfa["states"])} t\n'
    hoa += 'acc-name: all\n'
    hoa += 'tool: "FOLTDAR"\n'
    hoa += 'properties: trans-labels explicit-labels trans-acc deterministic\n'
    hoa += '--BODY--\n'
    for state in transByState:
        hoa += f'State: {state.replace("S", "")}\n'
        for lbl, nextS in transByState[state]:
            reward = False
            try:
                lbl, reward = eval(lbl)
            except (SyntaxError, NameError):
                reward = False
            if lbl == '':
                hoa += '[t] '
            else:
                hoa += f'[{add_a(lbl)}] '
            hoa += f'{nextS.replace("S", "")}'
            if reward:
                hoa += f' {"{"}{reward}{"}"}'
            hoa += '\n'
        hoa += '\n'
    hoa += '--END--\n'

    with open(f'{name}.hoa', 'w') as file:
        file.write(hoa)


def write_qrm(dfa, name):
    qrm = ''
    qrm += f'{dfa["initial_state"]}  # initial state\n'
    for tra in dfa['transitions']:
        ini = int(tra[0].replace('S', ''))
        end = int(dfa['transitions'][tra].replace('S', ''))
        try:
            lbl, reward = eval(tra[1])
        except (SyntaxError, NameError):
            lbl = tra[1]
            reward = 0
        lbl = lbl if lbl != '' else 'True'
        qrm += f'''({ini}, {end}, '{lbl}', ConstantRewardFunction({reward}))\n'''

    with open(f'{name}.txt', 'w') as file:
        file.write(qrm)


def write_output(output_type, dfa, name):
    if output_type == 'hoa':
        write_hoa(dfa, name)
    elif output_type == 'qrm':
        write_qrm(dfa, name)
