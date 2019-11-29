import networkx as netx
import netx.algorithms.isomorphism as iso
import sys


g1 = netx.nx_agraph.read_dot(f'{sys.argv[1]}.dot')
g2 = netx.nx_agraph.read_dot(f'{sys.argv[2]}.dot')
em = iso.cathegorical_edge_match('label', '')

print(netx.is_isomorphic(g1, g2))
