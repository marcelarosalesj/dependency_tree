"""
Basic Directed Graph using networkx
- can be saved as a dot file
- can be saved as postscript file
"""
import networkx as nx

G = nx.DiGraph()
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node('a')
G.add_edges_from([(1,2),(1,3),(3,4),(4,'a')])
pos=nx.spring_layout(G)

A = nx.nx_agraph.to_agraph(G)        # convert to a graphviz graph
X1 = nx.nx_agraph.from_agraph(A)     # convert back to networkx (but as Graph)
X2 = nx.Graph(A)          # fancy way to do conversion
G1 = nx.Graph(X1)          # now make it a Graph

A.write('k5.dot')     # write to dot file
X3 = nx.nx_agraph.read_dot('k5.dot')  # read from dotfile

A.layout()            # neato layout
A.draw("k5.ps")       # write postscript in k5.ps with neato layout
