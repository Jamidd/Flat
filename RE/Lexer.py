import ply.lex as lex


class MyLexer:

    reserved = {
        '|': 'ALT',
        '.': 'CONCAT',
        '*': 'STAR',
        '+': 'PLUS',
        '?': 'QUESTION',
        '@': 'EPSILON',
        'ϵ': 'EPS',
        '#': 'END',
        }

    # List of token names.   This is always required
    tokens = (
        'TERM',
        'LPAR',
        'RPAR',
    ) + tuple(reserved.values())

    # Regular expression rules for simple tokens

    t_ALT = r'\|'
    t_CONCAT = r'\.'
    t_STAR = r'\*'
    t_PLUS = r'\+'
    t_QUESTION = r'\?'
    t_EPSILON = r'\@'
    t_EPS = r'\ϵ'
    t_END = r'\#'
    t_LPAR = r'\('
    t_RPAR = r'\)'

    t_ignore = r' ' + '\n'

    def t_TERM(self, t):
        r'(?<![a-z])[_a-z0-9]+'
        t.type = MyLexer.reserved.get(t.value, 'TERM')
        return t  # Check for reserved words

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' in the input formula")
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
