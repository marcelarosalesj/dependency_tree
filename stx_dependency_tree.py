import glob
import networkx as nx
import re
import os
from pyrpm.spec import Spec # Other options?
import ipdb

specfiles = glob.glob('./**/*.spec', recursive=True)

G = nx.DiGraph()
count=0
for specfile in specfiles:
    # Create RPM Spec Object
    sp = Spec.from_file(specfile)
    # Get from path useful information
    stx_project = specfile.split('/stx/')[-1].split('/')[0]
    # Parse each of the packages in a spec file
    for pkg in sp.packages:
        G.add_node(pkg.name, path=specfile, project=stx_project)
        for br in pkg.build_requires:
            G.add_node(br, path=specfile, project=stx_project)
            G.add_edge(pkg.name, br)
        if sp.name == pkg.name:
            count = count +1
            for br in sp.build_requires:
                G.add_node(br, path=specfile, project=stx_project)
                G.add_edge(sp.name, br)

# Generating results
try:
    os.mkdir('results')
except FileExistsError as e:
    print('W: results directory already exists. Files will be overwritten.')
nx.write_graphml_xml(G, "results/xml")
nx.write_adjlist(G, 'results/adjlist')


print(count)


