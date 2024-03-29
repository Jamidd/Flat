
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftANDORIMPLIESDIMPLIESSINCErightYESTERDAYONCEHISTORICALLYrightNOTnonassocLPARRPARTERM NOT AND OR IMPLIES DIMPLIES LPAR RPAR TRUE FALSE YESTERDAY SINCE ONCE HISTORICALLY\n        formula : formula AND formula\n                | formula OR formula\n                | formula IMPLIES formula\n                | formula DIMPLIES formula\n                | formula SINCE formula\n                | YESTERDAY formula\n                | ONCE formula\n                | HISTORICALLY formula\n                | NOT formula\n                | TRUE\n                | FALSE\n                | TERM\n        \n        formula : LPAR formula RPAR\n        '
    
_lr_action_items = {'YESTERDAY':([0,2,3,4,5,9,10,11,12,13,14,],[2,2,2,2,2,2,2,2,2,2,2,]),'ONCE':([0,2,3,4,5,9,10,11,12,13,14,],[3,3,3,3,3,3,3,3,3,3,3,]),'HISTORICALLY':([0,2,3,4,5,9,10,11,12,13,14,],[4,4,4,4,4,4,4,4,4,4,4,]),'NOT':([0,2,3,4,5,9,10,11,12,13,14,],[5,5,5,5,5,5,5,5,5,5,5,]),'TRUE':([0,2,3,4,5,9,10,11,12,13,14,],[6,6,6,6,6,6,6,6,6,6,6,]),'FALSE':([0,2,3,4,5,9,10,11,12,13,14,],[7,7,7,7,7,7,7,7,7,7,7,]),'TERM':([0,2,3,4,5,9,10,11,12,13,14,],[8,8,8,8,8,8,8,8,8,8,8,]),'LPAR':([0,2,3,4,5,9,10,11,12,13,14,],[9,9,9,9,9,9,9,9,9,9,9,]),'$end':([1,6,7,8,15,16,17,18,20,21,22,23,24,25,],[0,-10,-11,-12,-6,-7,-8,-9,-1,-2,-3,-4,-5,-13,]),'AND':([1,6,7,8,15,16,17,18,19,20,21,22,23,24,25,],[10,-10,-11,-12,-6,-7,-8,-9,10,-1,-2,-3,-4,-5,-13,]),'OR':([1,6,7,8,15,16,17,18,19,20,21,22,23,24,25,],[11,-10,-11,-12,-6,-7,-8,-9,11,-1,-2,-3,-4,-5,-13,]),'IMPLIES':([1,6,7,8,15,16,17,18,19,20,21,22,23,24,25,],[12,-10,-11,-12,-6,-7,-8,-9,12,-1,-2,-3,-4,-5,-13,]),'DIMPLIES':([1,6,7,8,15,16,17,18,19,20,21,22,23,24,25,],[13,-10,-11,-12,-6,-7,-8,-9,13,-1,-2,-3,-4,-5,-13,]),'SINCE':([1,6,7,8,15,16,17,18,19,20,21,22,23,24,25,],[14,-10,-11,-12,-6,-7,-8,-9,14,-1,-2,-3,-4,-5,-13,]),'RPAR':([6,7,8,15,16,17,18,19,20,21,22,23,24,25,],[-10,-11,-12,-6,-7,-8,-9,25,-1,-2,-3,-4,-5,-13,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'formula':([0,2,3,4,5,9,10,11,12,13,14,],[1,15,16,17,18,19,20,21,22,23,24,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> formula","S'",1,None,None,None),
  ('formula -> formula AND formula','formula',3,'p_formula','Parser.py',25),
  ('formula -> formula OR formula','formula',3,'p_formula','Parser.py',26),
  ('formula -> formula IMPLIES formula','formula',3,'p_formula','Parser.py',27),
  ('formula -> formula DIMPLIES formula','formula',3,'p_formula','Parser.py',28),
  ('formula -> formula SINCE formula','formula',3,'p_formula','Parser.py',29),
  ('formula -> YESTERDAY formula','formula',2,'p_formula','Parser.py',30),
  ('formula -> ONCE formula','formula',2,'p_formula','Parser.py',31),
  ('formula -> HISTORICALLY formula','formula',2,'p_formula','Parser.py',32),
  ('formula -> NOT formula','formula',2,'p_formula','Parser.py',33),
  ('formula -> TRUE','formula',1,'p_formula','Parser.py',34),
  ('formula -> FALSE','formula',1,'p_formula','Parser.py',35),
  ('formula -> TERM','formula',1,'p_formula','Parser.py',36),
  ('formula -> LPAR formula RPAR','formula',3,'p_expr_group','Parser.py',62),
]
