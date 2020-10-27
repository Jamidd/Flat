import os
import sys
import apt
import re

sys.path.insert(1, './functions')

#  import and check all dependencies have been meet
try:
    import dd
    import ply
    import argparse
    from PySimpleAutomata import automata_IO as AutIO
    if not apt.Cache()['mona'].is_installed:
        raise ModuleNotFoundError
except ModuleNotFoundError:
    print("Dependencies have not been met. Please run 'sh dependencies.sh' on the terminal")
    if input("Do you want me to run it for you (y/n)").lower() in ["y", "yes"]:
        os.system("sh functions/dependencies.sh")
        print('-'*25)
        import dd
        import ply
        import argparse
        from PySimpleAutomata import automata_IO as AutIO
    else:
        exit()

from functions import automatas_to_rm, get_dfas, dfa_intersection_to_rm, read_formula, write_output

if __name__ == '__main__':
    def send_error(text, help=True):
        print(f"ERROR:\n{'-' * len(text)}\n{text}\n{'-' * len(text)}")
        if help:
            parser.print_help()
        exit()

    #  parse input
    parser = argparse.ArgumentParser(description='Translate Formal Languages to DFA or Reward Machines.')
    #parser.add_argument('-a', '--all', dest='all', action='store_true', default=False, help='Translate from all types of formulas (special restrictions added)')
    parser.add_argument('-l', '--ltlf', dest='ltlf', action='store_true', default=False, help='Translate LTLf formulas')
    parser.add_argument('-p', '--pltl', dest='pltl', action='store_true', default=False, help='Translate PLTL formulas')
    parser.add_argument('-w', '--pddl', dest='pddl', action='store_true', default=False, help='Translate PDDL3.0 constraint formulas')
    # parser.add_argument('-g', '--golog', dest='golog', action='store_true', default=False, help='Translate GOLOG formulas')
    # parser.add_argument('-d', '--ldlf', dest='ldlf', action='store_true', default=False, help='Translate LDLf formulas')
    # parser.add_argument('-t', '--tla', dest='tla', action='store_true', default=False, help='Translate TLA+ formulas')
    parser.add_argument('-e', '--re', dest='re', action='store_true', default=False, help='Translate Regular Expression formulas')
    parser.add_argument('-c', '--dfa', dest='dfa', action='store_true', default=False, help='Return DFA only')
    parser.add_argument('-m', '--rm', dest='rm', action='store_true', default=False, help='Return Reward Machine only (Default)')
    parser.add_argument('-b', '--dfarm', dest='dfarm', action='store_true', default=False, help='Return DFA and Reward Machine')
    parser.add_argument('-R', '--rmf', dest='rmf', action='store_true', default=False, help='Return reward machine in the same format as "https://bitbucket.org/RToroIcarte/rmf/src/master/"')
    parser.add_argument('-P', '--rmf2', dest='rmf2', action='store_true', default=False, help='Second version of Rodrigos Format, cannot be used with DFA')
    parser.add_argument('-D', '--dot', dest='dot', action='store_true', default=False, help='Return output as DOT file (Default)')
    parser.add_argument('-H', '--hoa', dest='hoa', action='store_true', default=False, help='Return output as HOA file')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', default=False, help='Do not print anything on screen (except errors)')
    parser.add_argument('-r', '--reduce', dest='reduce', action='store_true', default=False, help='Reduce Reward Machine or DFAs to accepting paths. If used with "-b" only reward machine will be reduced. Reward machine accepting states are the ones with highest reward.')
    parser.add_argument('-i', '--image', dest='image', action='store_true', default=False, help='Also save image of Reward Machine')
    parser.add_argument('-n', '--noshowreward', dest='noreward', action='store_true', default=False, help='Do not show reward. Can only be used with "-m". Reward has to always be added. If choosen in addition to "-r", the accepting states are still the ones with highest reward, even though they are later ignored.')
    parser.add_argument('-f', '--files', dest='files', default=[], nargs='+', type=str, help='Specify files to be taken into consideration, else all files with extension *.{language} in the directory will be selected.')

    # noreward solo con rm
    args = parser.parse_args()
    quiet = args.quiet
    #  cant select more than one language
    if [args.ltlf, args.pltl, args.pddl, args.re].count(True) != 1:
        send_error('You have to select only one language.')

    #  choose the output
    if [args.dfa, args.rm, args.dfarm].count(True) > 1:
        ll = 'You can only choose one type of output'
        print(f"ERROR:\n{'-'*len(ll)}\n{ll}\n{'-'*len(ll)}")
        parser.print_help()
        exit()
    elif args.dfa:
        dfa = True
        rm = False
    elif args.rm:
        dfa = False
        rm = True
    elif args.dfarm:
        dfa = True
        rm = True
    else:
        rm = True
        dfa = False

    reward = not args.noreward

    if reward and dfa:
        print('Rewards are not shown in DFAs')

    # select output
    if args.dot:
        output = 'dot'
    elif args.rmf:
        output = 'rmf'
    elif args.rmf2:
        output = 'rmf2'
    elif args.hoa:
        output = 'hoa'
    else:
        output = 'dot'

    #  select language
    if args.ltlf:
        extension = 'ltlf'
        sys.path.insert(1, './LTLf')
        if not quiet:
            print('LTLf option requested')
    elif args.pltl:
        extension = 'pltl'
        sys.path.insert(1, './PLTL')
        if not quiet:
            print('PLTL option requested')
    elif args.pddl:
        extension = 'pddl3'
        sys.path.insert(1, './PDDL3')
        if not quiet:
           print('PDDL3 option requested')
    # elif args.ldlf:
    #     # extension = 'ldlf'
    #     # sys.path.insert(1, './LDLf')
    #     # if not silence: print('LDLf option requested')
    #     print('Sorry, I have been too lazy to implement this yet. Good luck :-)')
    #     exit()
    # elif args.golog:
    #     # extension = 'golog'
    #     # sys.path.insert(1, './GOLOG')
    #     # if not silence: print('GOLOG option requested')
    #     print('Sorry, I have been too lazy to implement this yet. Good luck :-)')
    #     exit()
    # elif args.tla:
    #     # extension = 'tla'
    #     # sys.path.insert(1, './TLA')
    #     # if not silence: print('TLA+ option requested')
    #     print('Sorry, I have been too lazy to implement this yet. Good luck :-)')
    #     exit()
    elif args.re:
        extension = 're'
        sys.path.insert(1, './RE')
        if not quiet:
            print('RE option requested')
    elif args.all:
        print('Sorry, I have been too lazy to implement this yet. Good luck :-)')
        exit()

    #  import correct translator
    from Translator import Translator

    translator = Translator()
    formulas = []
    rewards = []

    #  if files are specified
    if len(args.files) > 0:

        for file in args.files:
            f_path = file.split('/')
            file = f_path[-1]
            
            #  add extension if it doesnt exist. If another extension is added, this will rule it out
            if re.match(f'[a-zA-Z1-9]+.{extension}', file) is None:
                file = file + extension
            
            f_path[-1] = file
            file = '/'.join(f_path)

            try:
                f, r = read_formula(file, extension)
            except FileNotFoundError:
                send_error(f'The file "{file}" is not in the directory', False)

            formulas += f
            rewards += r

    #  look for all the files
    else:
        for file in os.listdir():
            if re.match(f'[a-zA-Z1-9]+.{extension}', file) is not None:
                try:
                    f, r = read_formula(file)
                except:
                    send_error(f'There was an error reading the file: {file}')
                formulas += f
                rewards += r

    #  create required DFAs
    dfas = []
    for f in formulas:
        try:
            f = translator.translate(f, 'dfa.txt', quiet)
        except ValueError:
           send_error('There has been a problem, please check your formulas', False)

        if type(f) == list:
            dfas.extend(f)
        else:
            dfas.append(f)

    if extension == 'pddl3':
        rewards = [1]*len(dfas)

    # return
    if dfa and rm:
        dfas = get_dfas(dfas, rewards, reward=True, minimize=False)
        for i in range(len(dfas)):
            if output == 'dot' or args.image:
                AutIO.dfa_to_dot(dfas[i], f'DFA_{i}')
                if not args.image:
                    os.system(f'rm DFA_{i}.dot.svg')
                else:
                    os.system(f'mv DFA_{i}.dot.svg DFA_{i}.svg')
            if output != 'dot':
                os.system(f'rm DFA_{i}.dot')
                write_output(output, dfas[i], f'DFA_{i}')

        reward_machine = dfa_intersection_to_rm(dfas, args.reduce, reward)
        if output == 'dot' or args.image:
            AutIO.dfa_to_dot(reward_machine, 'RewardMachine')
            if not args.image:
                os.system('rm RewardMachine.dot.svg')
            else:
                os.system(f'mv RewardMachine.dot.svg RewardMachine.svg')
        if output != 'dot':
            os.system('rm RewardMachine.dot')
            write_output(output, reward_machine, 'RewardMachine')

    elif dfa:
        dfas = get_dfas(dfas, rewards, reward=False, minimize=args.reduce)
        for i in range(len(dfas)):
            if output == 'dot' or args.image:
                AutIO.dfa_to_dot(dfas[i], f'DFA_{i}')
                if not args.image:
                    os.system(f'rm DFA_{i}.dot.svg')
                else:
                    os.system(f'mv DFA_{i}.dot.svg DFA_{i}.svg')
                if output != 'dot':
                    os.system(f'rm DFA_{i}.dot')    
            if output != 'dot':
                write_output(output, dfas[i], f'DFA_{i}')

    elif rm:
        #  mix dfas and create the reward machine
        reward_machine = automatas_to_rm(dfas, rewards, args.reduce, reward)
        if output == 'dot' or args.image:
            AutIO.dfa_to_dot(reward_machine, 'RewardMachine')
            if not args.image:
                os.system('rm RewardMachine.dot.svg')
            else:
                os.system(f'mv RewardMachine.dot.svg RewardMachine.svg')
            if output != 'dot':
                os.system('rm RewardMachine.dot')
        if output != 'dot':
            write_output(output, reward_machine, 'RewardMachine')

    # os.system('rm dfa.txt')
    if 'formula.mona' in os.listdir():
        os.system('rm formula.mona')
