import ply.lex as lex


class MyLexer:

    reserved = {
        'true': 'TRUE',
        'false': 'FALSE',
        'last': 'LAST',
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
        'RPAR',
        'LCUBE',
        'RCUBE',
        'LDIAM',
        'RDIAM',
        'QUESTION',
        'PLUS',
        'SEMICOL',
        'STAR'
    ) + tuple(reserved.values())

    # Regular expression rules for simple tokens
    t_TRUE = r'true'
    t_FALSE = r'false'
    t_LAST = r'last'
    t_AND = r'\&'
    t_OR = r'\|'
    t_IMPLIES = r'\->'
    t_DIMPLIES = r'\<->'
    t_NOT = r'\~'
    t_LPAR = r'\('
    t_RPAR = r'\)'
    # LDLf specific
    t_LCUBE = r'\['
    t_RCUBE = r'\]'
    t_LDIAM = r'\<'
    t_RDIAM = r'\>'
    t_QUESTION = r'\?'
    t_PLUS = r'\+'
    t_SEMICOL = r'\;'
    t_STAR = r'\*'

    def t_TERM(self, t):
        r'(?<![a-z])(?!true|false|last)[_a-z0-9]+'
        t.type = MyLexer.reserved.get(t.value, 'TERM')
        return t  # Check for reserved words

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' in the input formula")
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
