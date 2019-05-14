import glob
import networkx as nx
import re
import os
from pyrpm.spec import Spec # Other options?
import ipdb
from networkx.algorithms.traversal.depth_first_search import dfs_edges
import argparse

parser = argparse.ArgumentParser(description='StarlingX Packages Dependency Graph')
parser.add_argument('-g','--generate', nargs=1,
                    help='Generate XML and dot. buildtime or runtime')
parser.add_argument('-s', '--search', nargs='?',
                    help='Search for Package Build RequirementsDependencies')
parser.add_argument('-i', '--input', nargs='?',
                    help='Input XML Graph')
parser.add_argument('-v', '--verbose',
                    help='Increase output verbosity',
                    action='count',
                    default=0)

specfiles = glob.glob('./**/*.spec', recursive=True)

def generate_graph(verbose=0, graphtype='buildtime'):
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
                G.add_node(pkg.name,
                           path=specfile,
                           project=stx_project,
                           ntype='stx_patched')
            else:
                """
                This case is when the node was previously created by another
                spec because it's a BuildRequires. Let's update its attributes.
                """
                if G.node[pkg.name]['ntype'] == 'non_stx_patched':
                    G.node[pkg.name]['path'] = specfile
                    G.node[pkg.name]['project'] = stx_project
                    G.node[pkg.name]['ntype'] = 'stx_patched'
            # Create BuildRequires or Requires Nodes
            if graphtype == 'buildtime':
                """
                Create BuildRequires Nodes and link them to the Package Node.
                Each Package Node must be linked to the Spec's BuildRequires
                and to it's own BuildRequires (if any).
                """
                if len(pkg.build_requires) and verbose == 1:
                    print("Package with extra BRs: {} in {}".format(pkg.name, specfile))

                build_requires = sp.build_requires + pkg.build_requires
                for br in build_requires:
                    if not G.has_node(br.name):
                        #If the Node does not exist already, it will create it.
                        G.add_node(br.name,
                                   path=specfile,
                                   project=stx_project,
                                   ntype='non_stx_patched')
                    G.add_edge(pkg.name, br.name)
            elif graphtype == 'runtime':
                """
                Create Requires Nodes and link them to the Package Node.
                Each Package Node must be linked to the Spec's Requires
                and to it's own Requires (if any).
                """
                if len(pkg.requires) and verbose == 1:
                    print("Package with extra Rs: {} in {}".format(pkg.name, specfile))

                requires = sp.requires + pkg.requires
                for r in requires:
                    if not G.has_node(r.name):
                        #If the Node does not exist already, it will create it.
                        G.add_node(r.name,
                                   path=specfile,
                                   project=stx_project,
                                   ntype='non_stx_patched')
                    G.add_edge(pkg.name, r.name)
            else:
                print('Not valid option: ', graphtype)
    return G

def search_dependencies(to_search, G, verbose):
    """
    Print dependencies
    """
    for edge in dfs_edges(G, to_search):
        print(edge)
        if verbose == 1:
            print(G.node[edge[0]])
            print(G.node[edge[1]])
            print('----------')

def write_graph(G, name):
    # Generating results
    try:
        os.mkdir('results')
    except FileExistsError as e:
        print('W: results directory already exists. Files will be overwritten.')
    nx.write_graphml_xml(G, "results/{}.xml".format(name))
    nx.drawing.nx_pydot.write_dot(G, "results/{}.dot".format(name))

def main():
    """
    Main tool
    """
    args = parser.parse_args()
    print(args)
    # Input Graph
    if args.generate:
        print('Generating {} graph'.format(args.generate[0]))
        G = generate_graph(args.verbose, args.generate[0])
        write_graph(G, args.generate[0])
    elif args.input:
        print('Input graph {}'.format(args.input))
        G = nx.read_graphml(args.input)
    else:
        print('It was not provide any graph. Use --generate or --input.')
        exit(1)
    # Search Dependencies
    if args.search:
        search_dependencies(args.search, G, args.verbose)

if __name__ == '__main__':
    main()
