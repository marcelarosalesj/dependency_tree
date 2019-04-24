import glob
import networkx as nx
import re
import os
from pyrpm.spec import Spec # Other options?
import ipdb

files = glob.glob('./**/*.spec', recursive=True)

G = nx.DiGraph()
count=0
for ff in files:
    with open(ff) as spec:
        # Create RPM Spec Object
        ss = Spec.from_file(ff)
        # Get from path useful information
        packagespec = ff.split('/')[-1].split('.')[0] # get name of spec...
        attr_path = ff
        attr_project = ff.split('/stx/')[-1].split('/')[0] # get name of project
        # Parse each of the packages in a spec file
        for pkg in ss.packages:
            G.add_node(pkg.name, path=attr_path, project=attr_project)
            for br in pkg.build_requires:
                G.add_node(br, path=attr_path, project=attr_project)
                G.add_edge(pkg.name, br)
            if ss.name == pkg.name:
                count = count +1
                for br in ss.build_requires:
                    G.add_node(br, path=attr_path, project=attr_project)
                    G.add_edge(ss.name, br)



pos=nx.spring_layout(G)
# Generating some results
try:
    os.mkdir('results')
except FileExistsError as e:
    print('W: results directory already exists. Files will be overwritten.')
nx.write_graphml_xml(G, "results/xml")
nx.write_adjlist(G, 'results/adjlist')


print(count)


