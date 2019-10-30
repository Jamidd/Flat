import ply.yacc as yacc
from Lexer import MyLexer


class MyParser(object):

    precedence = (
        ('left', 'AND', 'OR', 'IMPLIES', 'DIMPLIES', 'UNTIL'),
        ('right', 'NEXT', 'EVENTUALLY', 'GLOBALLY'),
        ('right', 'NOT'),
        ('nonassoc', 'LPAR', 'RPAR')
    )

    def __init__(self):
        self.lexer = MyLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    def __call__(self, s, **kwargs):
        return self.parser.parse(s, lexer=self.lexer.lexer)

    def p_formula(self, p):
        '''
        formula : formula AND formula
                | formula OR formula
                | formula IMPLIES formula
                | formula DIMPLIES formula
                | formula UNTIL formula
                | NEXT formula
                | EVENTUALLY formula
                | GLOBALLY formula
                | NOT formula
                | TRUE
                | FALSE
                | TERM
        '''

        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            if p[1] == 'F':  # eventually A == true UNITL A
                p[0] = ('U', 'true', p[2])
            elif p[1] == 'G':  # globally A == not( eventually (not A) )
                p[0] = ('~', ('U', 'true', ('~', p[2])))
            else:
                p[0] = (p[1], p[2])

        elif len(p) == 4:
            if p[2] == '->':
                p[0] = ('|', ('~', p[1]), p[3])
            elif p[2] == '<->':
                p[0] = ('&', ('|', ('~', p[1]), p[3]), ('|', ('~', p[3]), p[1]))
            else:
                p[0] = (p[2], p[1], p[3])
        else:
            raise ValueError

    def p_expr_group(self, p):
        '''
        formula : LPAR formula RPAR
        '''
        p[0] = p[2]

    def p_error(self, p):
        raise ValueError(f"Syntax error in input! {p}")
