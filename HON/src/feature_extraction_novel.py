"""
Script for extraction of the novel features from HON
"""

from __future__ import print_function, division

import networkx as nx
import sys
from pprint import pprint
import os
import csv
import numpy as np


def getFileName(dirname, musictype):
    fnames = [f for f in os.listdir(
        dirname) if os.path.isfile(os.path.join(dirname, f))]
    fnames = [f for f in fnames if f.startswith(musictype)]
    return fnames


def getGMLNetwork(fname):
    """
    Read the network stored as GML
    """
    return nx.read_gml(fname)


def getAbruptness(graph):
    """
    Edges with high betweeness but low transition prob

    Defined as betweenss/prob
    """
    unweighted_edge_betweeness = nx.edge_betweenness_centrality(
        graph, normalized=True)
    weighted_edge_betweeness = nx.edge_betweenness_centrality(
        graph, normalized=True, weight='weight')
    transition_prob = graph.edges(data=True)

    unweighted_abruptness = {}
    weighted_abruptness = {}

    for edge in transition_prob:
        unweighted_abruptness[(edge[0], edge[1])] = unweighted_edge_betweeness[
            (edge[0], edge[1])] / edge[2]['weight']
        weighted_abruptness[(edge[0], edge[1])] = weighted_edge_betweeness[
            (edge[0], edge[1])] / edge[2]['weight']

    return unweighted_abruptness.values(), weighted_abruptness.values()


def getBranchisess(graph, tau=0.1):
    """
    Unweighted out-degree counting only edges with weight greater than tau
    """

    # Edges with weight greater than tau
    edges = [(e[0], e[1])
             for e in graph.edges(data=True) if e[2]['weight'] > tau]

    sg = nx.Graph()
    sg.add_edges_from(edges)
    # add nodes in case there are nodes which are not included in edges
    sg.add_nodes_from(graph.nodes())

    degree = nx.degree(sg)
    return [d[1] for d in degree]


def getRepeatedness(graph, tau=0.75):
    """
    Unweighted chaings of edge weight greather than tau
    """
    edges = [(e[0], e[1])
             for e in graph.edges(data=True) if e[2]['weight'] > tau]
    edge_weight = nx.get_edge_attributes(graph, "weight")
    sg = nx.DiGraph()
    sg.add_edges_from(edges)
    nx.set_edge_attributes(sg, edge_weight, "weight")
    # find paths that is likely to occur (transition probability is higher)
    # inverse weight to find longest path
    from itertools import permutations
    edge_weight = nx.get_edge_attributes(sg, "weight")
    node_pairs = permutations(list(sg.nodes()), 2)
    path_dict = {}
    for (n1, n2) in node_pairs:
        paths = list(nx.all_simple_paths(sg, source=n1, target=n2))
        for each_path in paths:
            edges = zip(each_path[:-1], each_path[1:])
            prob = sum([edge_weight[edge] for edge in edges])
            path_dict[','.join(each_path)] = prob
    return path_dict


def getMelodic(graph):
    nodes = list(graph.nodes())
    rule_length_list = []
    for node in nodes:
        previous_nodes = node.split('|')[1].split('.')
        if previous_nodes == ['']:
            length = 1
        else:
            length = len(previous_nodes) + 1
        rule_length_list.append(length)
    return rule_length_list


def getPitchRange(graph):
    import itertools
    nodes = list(graph.nodes())
    pitch_in_rules = []
    for node in nodes:
        current_node = node.split('|')[0]
        previous_nodes = node.split('|')[1].split('.')
        if previous_nodes == ['']:
            pitches = [int(current_node)]
        else:
            pitches = [int(current_node)] + list(map(int, previous_nodes))
        pitch_in_rules.append(pitches)
    pitch_range_in_rules = []
    for pitches in pitch_in_rules:
        pitch_range_in_rules.append(max(pitches) - min(pitches))
    pitches_in_piece = list(itertools.chain(*pitch_in_rules))
    pitch_range_of_piece = max(pitches_in_piece) - min(pitches_in_piece)
    return pitch_range_in_rules, pitch_range_of_piece


def saveData(sname, data):
    dkeys = data.keys()
    tdata = [dkeys]

    for i in xrange(0, max([len(data[d]) for d in data])):
        row = []

        for d in dkeys:
            if len(data[d]) > i:
                row.append(data[d][i])
            else:
                row.append(None)
        tdata.append(row)

    with open(sname, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for row in tdata:
            writer.writerow(row)

if __name__ == '__main__':
    dirname = sys.argv[1]			# GML dirname
    sname = sys.argv[2]				# Save file name
    musictype = sys.argv[3] 		# Music Type

    data = {}
    data['unweighted_abruptness'] = []
    data['weighted_abruptness'] = []
    data['branchiness'] = []

    for f in getFileName(dirname, musictype):
        print(f)
        graph = getGMLNetwork(os.path.join(dirname, f))

        d0, d1 = getAbruptness(graph)
        d2 = getBranchisess(graph, 0.1)

        # print(d0)
        #data['unweighted_abruptness'] += d0
        # print(data['unweighted_abruptness'])
        #data['weighted_abruptness'] += d1
        #data['branchiness'] += d2

        data['unweighted_abruptness'].append(np.percentile(d0, 95))
        data['weighted_abruptness'].append(np.percentile(d1, 95))
        data['branchiness'].append(np.mean(d2))

    saveData(sname, data)
