import glob
import networkx as nx
import re
import os

files = glob.glob('./**/*.spec', recursive=True)

G = nx.DiGraph()

for f in files:
    with open(f) as spec:
        packagespec = f.split('/')[-1].split('.')[0]
        attr_path = f
        attr_project = f.split('/stx/')[-1].split('/')[0]
        G.add_node(packagespec, path=attr_path, project=attr_project)
        for line in spec.readlines():
            r1 = re.match(r"^BuildRequires:", line)
            if r1 is not None:
                buildreq = line.split('BuildRequires:')[-1].strip()
                G.add_edge(packagespec, buildreq)

pos=nx.spring_layout(G)

# Generating some results
try:
    os.mkdir('results')
except FileExistsError as e:
    print('W: results directory already exists. Files will be overwritten.')
nx.write_graphml_xml(G, "results/xml")
nx.write_adjlist(G, 'results/adjlist')



