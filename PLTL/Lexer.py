import ply.lex as lex


class MyLexer:

    reserved = {
        'and': 'WAND',
        'or': 'WOR',
        'not': 'WNOT',
        'true': 'TRUE',
        'false': 'FALSE',
        'Y': 'YESTERDAY',
        'S': 'SINCE',
        'O': 'ONCE',
        'H': 'HISTORICALLY',
        'YESTERDAY': 'UYESTERDAY',
        'SINCE': 'USINCE',
        'ONCE': 'UONCE',
        'HISTORICALLY': 'UHISTORICALLY',
        'yesterday': 'LYESTERDAY',
        'since': 'LSINCE',
        'once': 'LONCE',
        'historically': 'LHISTORICALLY'
    }
    # List of token names.   This is always required
    tokens = (
        'TERM',
        'NOT',
        'AND',
        'OR',
        'IMPLIES',
        'DIMPLIES',
        'LPAR',
        'RPAR'
    ) + tuple(reserved.values())

    # Regular expression rules for simple tokens
    t_TRUE = r'true'
    t_FALSE = r'false'
    t_AND = r'\&'
    t_WAND = 'and'
    t_OR = r'\|'
    t_WOR = 'or'
    t_IMPLIES = r'\->'
    t_DIMPLIES = r'\<->'
    t_NOT = r'\~'
    t_WNOT = 'not'
    t_LPAR = r'\('
    t_RPAR = r'\)'
    # PAST OPERATOR
    t_YESTERDAY = r'Y'
    t_SINCE = r'S'
    t_ONCE = r'O'
    t_HISTORICALLY = r'H'
    t_UYESTERDAY = r'YESTERDAY'
    t_USINCE = r'SINCE'
    t_UONCE = r'ONCE'
    t_UHISTORICALLY = r'HISTORICALLY'
    t_LYESTERDAY = r'yesterday'
    t_LSINCE = r'since'
    t_LONCE = r'once'
    t_LHISTORICALLY = r'historically'

    t_ignore = r' ' + '\n'

    def t_TERM(self, t):
        r'(?<![a-z])(?!true|false)[_a-z0-9]+'
        t.type = MyLexer.reserved.get(t.value, 'TERM')
        return t  # Check for reserved words

    def t_error(self, t):
        print("Illegal character '%s' in the input formula" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
