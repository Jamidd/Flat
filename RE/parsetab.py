
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rightALTleftCONCATleftSTARPLUSQUESTIONnonassocLPARRPARALT CONCAT END EPS EPSILON LPAR PLUS QUESTION RPAR STAR TERM\n        element : TERM\n        \n        element : END\n        \n        element : element STAR\n                | element ALT element\n                | element CONCAT element\n        \n        element : EPSILON\n                | EPS\n        \n        element : element PLUS\n        \n        element : element QUESTION\n        \n        element : LPAR element RPAR\n        '
    
_lr_action_items = {'TERM':([0,6,8,9,],[2,2,2,2,]),'END':([0,6,8,9,],[3,3,3,3,]),'EPSILON':([0,6,8,9,],[4,4,4,4,]),'EPS':([0,6,8,9,],[5,5,5,5,]),'LPAR':([0,6,8,9,],[6,6,6,6,]),'$end':([1,2,3,4,5,7,10,11,13,14,15,],[0,-1,-2,-6,-7,-3,-8,-9,-4,-5,-10,]),'STAR':([1,2,3,4,5,7,10,11,12,13,14,15,],[7,-1,-2,-6,-7,-3,-8,-9,7,7,7,-10,]),'ALT':([1,2,3,4,5,7,10,11,12,13,14,15,],[8,-1,-2,-6,-7,-3,-8,-9,8,8,-5,-10,]),'CONCAT':([1,2,3,4,5,7,10,11,12,13,14,15,],[9,-1,-2,-6,-7,-3,-8,-9,9,9,-5,-10,]),'PLUS':([1,2,3,4,5,7,10,11,12,13,14,15,],[10,-1,-2,-6,-7,-3,-8,-9,10,10,10,-10,]),'QUESTION':([1,2,3,4,5,7,10,11,12,13,14,15,],[11,-1,-2,-6,-7,-3,-8,-9,11,11,11,-10,]),'RPAR':([2,3,4,5,7,10,11,12,13,14,15,],[-1,-2,-6,-7,-3,-8,-9,15,-4,-5,-10,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'element':([0,6,8,9,],[1,12,13,14,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> element","S'",1,None,None,None),
  ('element -> TERM','element',1,'p_ter','Parser.py',28),
  ('element -> END','element',1,'p_end','Parser.py',42),
  ('element -> element STAR','element',2,'p_formula','Parser.py',49),
  ('element -> element ALT element','element',3,'p_formula','Parser.py',50),
  ('element -> element CONCAT element','element',3,'p_formula','Parser.py',51),
  ('element -> EPSILON','element',1,'p_eps','Parser.py',64),
  ('element -> EPS','element',1,'p_eps','Parser.py',65),
  ('element -> element PLUS','element',2,'p_plu','Parser.py',72),
  ('element -> element QUESTION','element',2,'p_quest','Parser.py',79),
  ('element -> LPAR element RPAR','element',3,'p_expr_group','Parser.py',86),
]
