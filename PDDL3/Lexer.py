import ply.lex as lex


class MyLexer:

    reserved = {
        'and': 'AND',
        'not': 'NOT',
        'at-end': 'ATEND',
        'always': 'ALWAYS',
        'sometime': 'SOMETIME',
        'within': 'WITHIN',
        'at-most-once': 'ATMOSTONCE',
        'sometime-after': 'SOMETIMEAFTER',
        'sometime-before': 'SOMETIMEBEFORE',
        'always-within': 'ALWAYSWITHIN',
        'hold-during': 'HOLDDURING',
        'hold-after': 'HOLDAFTER',
        'implies': 'IMPLIES',
        'forall': 'FORALL',
        'exists': 'EXISTS',
        '?': 'VAR',
        '-': 'TYP',
        '(': 'LPAR',
        ')': 'RPAR'
    }

    # List of token names.   This is always required
    tokens = (
        'TERM',
        'NUM'
    ) + tuple(reserved.values())

    # Regular expression rules for simple tokens

    t_AND = 'and'
    t_NOT = 'not'
    t_LPAR = r'\('
    t_RPAR = r'\)'
    t_VAR = r'\?'
    t_ATEND = r'at-end'
    t_ALWAYS = r'always'
    t_SOMETIME = r'sometime'
    t_WITHIN = r'within'
    t_ATMOSTONCE = r'at-most-once'
    t_SOMETIMEAFTER = r'sometime-after'
    t_SOMETIMEBEFORE = r'sometime-before'
    t_ALWAYSWITHIN = r'always-within'
    t_IMPLIES = r'implies'
    t_ignore = r' ' + '\n'

    def t_NUM(self, t):
        r'(\d)[0-9.]*'
        t.type = MyLexer.reserved.get(t.value, 'NUM')
        return t  

    def t_TERM(self, t):
        r'[<>=+\-a-zA-Z][<>=+\-0-9a-zA-Z]*'
        t.type = MyLexer.reserved.get(t.value, 'TERM')
        return t 

    def t_error(self, t):
        # print(f"Illegal character '{t.value[0]}' in the input formula")
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
