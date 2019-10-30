import ply.yacc as yacc
from Lexer import MyLexer


class MyParser(object):

    precedence = (
        ('left', 'AND', 'OR', 'IMPLIES', 'DIMPLIES', 'PLUS', 'SEMICOL'),
        ('left', 'QUESTION', 'STAR'),
        ('right', 'NOT'),
        ('nonassoc', 'LCUBE', 'RCUBE', 'LDIAM', 'RDIAM'),
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
                | formula PLUS formula
                | formula SEMICOL formula
                | formula QUESTION
                | formula STAR
                | NOT formula
                | TRUE
                | FALSE
                | LAST
                | TERM
        '''

        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
        	if p[1] == '~':
        		p[0] = ('~', p[2])
        	else:
        		p[0] = (p[2], p[1])
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

    def p_modal_conect(self, p):
        '''
        formula : LCUBE formula RCUBE formula
        		| LDIAM formula RDIAM formula
        '''
        if p[1] == '[':
            p[0] = ('[]', p[2], p[4])
        	#p[0] = ('~', ('<>', p[2], ('~', p[4])))
        elif p[1] == '<':
        	p[0] = ('<>', p[2], p[4])

    def p_error(self, p):
        raise ValueError(f"Syntax error in input! {p}")
