import ply.yacc as yacc
from Lexer import MyLexer


class MyParser(object):

    precedence = (
        ('right', 'FORALL', 'EXISTS', \
            'ALWAYS', 'SOMETIME', 'WITHIN', 'ATMOSTONCE', \
            'SOMETIMEAFTER', 'SOMETIMEBEFORE', 'ALWAYSWITHIN', \
            'HOLDDURING', 'HOLDAFTER'),
        ('left', 'VAR', 'TYP'),
        ('nonassoc', 'LPAR', 'RPAR')
    )

    def __init__(self):
        self.lexer = MyLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    def __call__(self, s, **kwargs):
        return self.parser.parse(s, lexer=self.lexer.lexer, debug=False)

    def p_formula(self, p):
        '''
        formula : AND list_f
                | ATEND formula
                | ALWAYS formula
                | SOMETIME formula
                | WITHIN NUM formula
                | ATMOSTONCE formula
                | SOMETIMEAFTER formula formula
                | SOMETIMEBEFORE formula formula
                | ALWAYSWITHIN NUM formula formula
                | IMPLIES formula formula
                | NOT formula
                | HOLDDURING NUM NUM formula
                | HOLDAFTER NUM formula
                | FORALL list_v formula
                | formula TERM
                | vars
                | list_p
        '''
        if len(p) == 2:
            p[0] = p[1]

        elif len(p) == 3:
            p[0] = (p[1], p[2])

        elif len(p) == 4:
            p[1] = p[1]
            p[0] = (p[1], p[2], p[3])

        elif len(p) == 5:
            p[0] = (p[1], p[2], p[3], p[4])
        else:
            raise ValueError

    def p_params(self, p):
        '''
        param : TERM
              | NUM
              | VAR TERM
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[1]+p[2])

    def p_lparams(self, p):
        '''
        list_p : param
                | param param
                | list_p param
                | list_p formula
        '''
        if len(p) == 2:
            p[0] = (p[1], )
        elif type(p[1]) != tuple:
            p[0] = tuple([p[1], p[2]])
        else:
            aa = list(p[1])
            if type(p[2]) != tuple:
                aa.append(p[2])
                p[0] = tuple(aa)
            else:
                bb = list(p[2])
                p[0] = tuple(aa+bb)

    def p_vars(self, p):
        '''
        vars : VAR TERM TYP TERM
        '''
        p[0] = (p[1]+p[2], p[3], p[4])

    def p_lvars(self, p):
        '''
        list_v : vars
                | vars vars
                | list_v vars
                | LPAR list_v RPAR
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = tuple(list(p[1])+list(p[2]))
        else:
            p[0] = p[2]

    def p_list_formulas(self, p):
        '''
        list_f : formula
               | formula formula
               | list_f formula
        '''
        if len(p) == 2:
            p[0] = (p[1],)
        elif p.slice[1].type == 'formula':
            p[0] = tuple([p[1], p[2]])
        else:
            aa = list(p[1])
            aa.append(p[2])
            p[0] = tuple(aa)

    def p_expr_group(self, p):
        '''
        formula : LPAR formula RPAR
                | LPAR list_p RPAR
        '''
        p[0] = p[2]

    def p_error(self, p):
        raise ValueError(f"Syntax error in input! {p}")
