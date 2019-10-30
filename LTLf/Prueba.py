from Translator import Translator

formula = "G~a&F(c&XFo)"  # &G(c->XG(o<->(~Xtrue)))"#&F(c&XF(o))"#&G(c->XG(o<->(~Xtrue)))"
declare_flag = False  # True if you want to compute DECLARE assumption for the formula

trans = Translator()
print(trans(formula))

