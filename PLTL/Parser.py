import ply.yacc as yacc
from Lexer import MyLexer


class MyParser(object):

    precedence = (
        ('left', 'AND', 'OR', 'IMPLIES', 'DIMPLIES', 'SINCE'),
        ('right', 'YESTERDAY', 'ONCE', 'HISTORICALLY'),
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
                | formula SINCE formula
                | YESTERDAY formula
                | ONCE formula
                | HISTORICALLY formula
                | NOT formula
                | TRUE
                | FALSE
                | TERM
        '''

        if len(p) == 2:
            p[0] = p[1]

        elif len(p) == 3:
            if p[1] == 'O':  # ONCE A = true SINCE A
                p[0] = ('S', 'true', p[2])
            elif p[1] == 'H':  # HISTORICALLY A == not( ONCE (not A) )
                p[0] = ('~', ('S', 'true', ('~', p[2])))
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
        raise ValueError("Syntax error in input! %s" % str(p))
