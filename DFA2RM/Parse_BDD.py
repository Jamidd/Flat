from dd import bdd as BDD
from ast import literal_eval

vocab = ['A', 'B', 'C', 'D']

bdd = BDD.BDD()
bdd.declare(*vocab)

b = bdd.add_expr('A->B|B|C')
bdd.to_expr(b)