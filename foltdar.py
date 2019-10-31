import os
import sys
import apt
import re

sys.path.insert(1, './DFA2RM')

#  import and check all dependencies have been meet
try:
    import dd
    import ply
    import argparse
    from PySimpleAutomata import automata_IO as AutIO
    if apt.Cache()['mona'].is_installed != True:
        raise ModuleNotFoundError
except ModuleNotFoundError:
    print("Dependencies have not been met. Please run 'sh dependecies.sh' on the terminal")
    if input("Do you want me to run it for you (y/n)").lower() in ["y", "yes"]:
        os.system("sh DFA2RM/dependencies.sh")
        print('-'*25)
        import dd
        import ply
        import argparse
        from PySimpleAutomata import automata_IO as AutIO
    else:
        exit()

from dfa2rm import automatas_to_rm, get_dfas, dfa_intersection_to_rm, read_formula

if __name__ == '__main__':
    #  parse input
    parser = argparse.ArgumentParser(description='Translate Formal Lenguages to DFA or Reward Machines.')
    parser.add_argument('-a', '--all', dest='all', action='store_true', default=False, help='Translate from all types of formulas (special restrictions added)')
    parser.add_argument('-l', '--ltlf', dest='ltlf', action='store_true', default=False, help='Translate LTLf formulas')
    parser.add_argument('-p', '--pltl', dest='pltl', action='store_true', default=False, help='Translate PLTL formulas')
    parser.add_argument('-g', '--golog', dest='golog', action='store_true', default=False, help='Translate GOLOG formulas')
    parser.add_argument('-d', '--ldlf', dest='ldlf', action='store_true', default=False, help='Translate LDLf formulas')
    parser.add_argument('-t', '--tla', dest='tla', action='store_true', default=False, help='Translate TLA+ formulas')
    parser.add_argument('-e', '--re', dest='re', action='store_true', default=False, help='Translate Regular Expression formulas')
    parser.add_argument('-c', '--dfa', dest='dfa', action='store_true', default=False, help='Return DFA only')
    parser.add_argument('-m', '--rm', dest='rm', action='store_true', default=False, help='Return Reward Machine only (Default)')
    parser.add_argument('-b', '--dfarm', dest='dfarm', action='store_true', default=False, help='Return DFA and Reward Machine')
    parser.add_argument('-z', '--qrm', dest='qrm', action='store_true', default=False, help='Represent reward machine in the same format as "https://bitbucket.org/RToroIcarte/qrm/src/master/"')    
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', default=False, help='Do not print anything on screen (except errors)')
    parser.add_argument('-r', '--reduce', dest='reduce', action='store_true', default=False, help='Reduce Reward Machine or DFAs to accepting paths. If used with "-b" only reward machine will be reduced.')
    parser.add_argument('-i', '--image', dest='image', action='store_true', default=False, help='Also save image of Reward Machine')
    parser.add_argument('-n', '--noreward', dest='noreward', action='store_true', default=False, help='Do not consider reward. Can only be used with "-c". Reward still has to be added, but just set it to 0')
    parser.add_argument('-f', '--files', dest='files', default=[], nargs='+', type=str, help='Specify files to be taken into consideration, else all files with extention *.{language} in the directory will be selected.')

    args = parser.parse_args()
    quiet = args.quiet
    #  cant selct more than one language
    if [args.all, args.ltlf, args.pltl, args.golog, args.ldlf, args.tla].count(True) != 1:
        ll = 'You have to select only one language. No more no less.'
        print(f"ERROR:\n{'-'*len(ll)}\n{ll}\n{'-'*len(ll)}")
        parser.print_help()
        exit()

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

    #  select lenguage
    if args.ltlf:
        extention = 'ltlf'
        sys.path.insert(1, './LTLf')
        if not quiet:
            print('LTLf option requested')
    elif args.pltl:
        extention = 'pltl'
        sys.path.insert(1, './PLTL')
        if not quiet:
            print('PLTL option requested')
    elif args.ldlf:
        # extention = 'ldlf'
        # sys.path.insert(1, './LDLf')
        # if not silence: print('LDLf option requested')
        print('Sorry, I have been to lazy to implement this yet. Good luck :-)')
        exit()
    elif oargs.golog:
        # extention = 'golog'
        # sys.path.insert(1, './GOLOG')
        # if not silence: print('GOLOG option requested')
        print('Sorry, I have been to lazy to implement this yet. Good luck :-)')
        exit()
    elif args.tla:
        # extention = 'tla'
        # sys.path.insert(1, './TLA')
        # if not silence: print('TLA+ option requested')
        print('Sorry, I have been to lazy to implement this yet. Good luck :-)')
        exit()
    elif args.re:
        # extention = 're'
        # sys.path.insert(1, './RE')
        # if not silence: print('RE option requested')
        print('Sorry, I have been to lazy to implement this yet. Good luck :-)')
        exit()
    elif args.all:
        print('Sorry, I have been to lazy to implement this yet. Good luck :-)')
        exit()

    #  import correct translator
    from Translator import Translator

    translator = Translator()
    formulas = []
    rewards = []

    #  if files are specified
    if len(args.files) > 0:

        for file in args.files:
            #  add extention if it doesnt exist. If another extention is added, this will rule it out
            if re.match(f'[a-zA-Z1-9]+.{extention}', file) is None:
                file = file + extention
            try:
                f, r = read_formula(file)
            except FileNotFoundError:
                print(f'The file {file} is not in the directory')
                exit()

            formulas += f
            rewards += r

    #  look for all the files
    else:
        for file in os.listdir():
            if re.match(f'[a-zA-Z1-9]+.{extention}', file) is not None:
                f, r = read_formula(file)
                formulas += f
                rewards += r

    #  create required DFAs
    dfas = []
    for f in formulas:
        # TODO revisar
        translator.pass_trough_mona(f, quiet)

        try:
            f = translator.read_dfa('dfa.txt')
        except:
            print('Problem with mona, please check your formulas')
            exit()
        dfas.append(f)

    # return
    if dfa and rm:
        dfas = get_dfas(dfas, r, reward = True, minimize = False)
        for i in range(len(dfas)):
            AutIO.dfa_to_dot(dfas[i], f'SuperDFA_{i}')
            if not args.image:
                os.system(f'rm SuperDFA_{i}.dot.svg')

        reward_machine = dfa_intersection_to_rm(dfas, args.reduce)
        AutIO.dfa_to_dot(reward_machine, 'RewardMachine') 
        if not args.image:
            os.system('rm RewardMachine.dot.svg')

    elif dfa:
        dfas = get_dfas(dfas, r, reward, args.reduce)
        for i in range(len(dfas)):
            AutIO.dfa_to_dot(dfas[i], f'SuperDFA_{i}')
            if not args.image:
                os.system(f'rm SuperDFA_{i}.dot.svg')

    elif rm:
        #  mix dfas and create the reward machine
        reward_machine = automatas_to_rm(dfas, rewards, args.reduce)
        AutIO.dfa_to_dot(reward_machine, 'RewardMachine') 
        if not args.image:
            os.system('rm RewardMachine.dot.svg')

    os.system('rm dfa.txt')
    os.system('rm formula.mona')
