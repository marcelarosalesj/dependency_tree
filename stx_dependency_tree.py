import glob
import networkx as nx
import re
import os
from pyrpm.spec import Spec # Other options?
import ipdb

specfiles = glob.glob('./**/*.spec', recursive=True)

G = nx.DiGraph()
for specfile in specfiles:
    sp = Spec.from_file(specfile)
    stx_project = specfile.split('/stx/')[-1].split('/')[0]
    for pkg in sp.packages:
        # Create Package Node
        if not G.has_node(pkg.name):
            """
            For this logic I'm assuming a package is generated only by one
            specfile.
            Ex: it won't be a case where stx-one has a spec where fm.deb
            is generated and stx-two has another spec generating fm.deb.
            """
            G.add_node(pkg.name, path=specfile, project=stx_project)
        else:
            """
            This case is when the node was previously created by another spec
            because it's a BuildRequires. Let's update its attributes.
            """
            G.node[pkg.name]['path'] = specfile
            G.node[pkg.name]['project'] = stx_project

        """
        Create BuildRequires Nodes and link them to the Package Node.
        Each Package Node must be linked to the Spec's BuildRequires
        and to it's own BuildRequires (if any).
        """
        if len(pkg.build_requires):
            print("Package with extra BRs: {} in {}".format(pkg.name, specfile))

        build_requires = sp.build_requires + pkg.build_requires
        for br in build_requires:
            G.add_node(br.name, path=specfile, project=stx_project)
            G.add_edge(pkg.name, br.name)

# Generating results
try:
    os.mkdir('results')
except FileExistsError as e:
    print('W: results directory already exists. Files will be overwritten.')
nx.write_graphml_xml(G, "results/xml")
nx.write_adjlist(G, 'results/adjlist')


