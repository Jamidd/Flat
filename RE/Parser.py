import ply.yacc as yacc
from Lexer import MyLexer

class MyParser(object):

    precedence = (
        ('right', 'ALT'),
        ('left', 'CONCAT'),
        ('left', 'STAR', 'PLUS', 'QUESTION'),
        ('nonassoc', 'LPAR', 'RPAR')
    )

    def __init__(self):
        self.lexer = MyLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.change_dict = {}
        self.name_num = 97
        self.prev = ''


    def __call__(self, s, **kwargs):
        return self.parser.parse(s, lexer=self.lexer.lexer, debug=False)

    def p_ter(self, p):
        '''
        element : TERM
        '''
        p[0] = self.prev + chr(self.name_num)
        self.change_dict[self.prev + chr(self.name_num)] = p[1]

        self.name_num += 1
        if self.name_num > 122:
            self.prev += '@'
            self.name_num = 97

    def p_end(self, p):
        '''
        element : END
        '''
        p[0] = p[1]
        self.change_dict[p[1]] = p[1]

    def p_formula(self, p):
        '''
        element : element STAR
                | element ALT element
                | element CONCAT element
        '''
        if len(p) == 3:
            p[0] = (p[2], p[1])

        elif len(p) == 4:
            p[0] = (p[2], p[1], p[3])

        else:
            raise ValueError

    def p_eps(self, p):
        '''
        element : EPSILON
                | EPS
        '''
        p[0] = self.prev + chr(self.name_num)
        self.change_dict[self.prev + chr(self.name_num)] = 'ϵ'

        self.name_num += 1
        if self.name_num > 122:
            self.prev += '@'
            self.name_num = 97

    def p_plu(self, p):
        '''
        element : element PLUS
        '''

        p[0] = ('.', p[1], ('*', p[1]))

    def p_quest(self, p):
        '''
        element : element QUESTION
        '''

        p[0] = ('|', p[1], 'ϵ')

    def p_expr_group(self, p):
        '''
        element : LPAR element RPAR
        '''

        p[0] = p[2]

    def p_error(self, p):

        raise ValueError(f"Syntax error in input! {p}")
