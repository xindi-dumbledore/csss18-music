"""
Script for extraction of features from HON
"""

from __future__ import print_function, division
import networkx as nx
import numpy as np
import community
from itertools import permutations
import itertools
import time


def getPitchesGivenRules(rule):
    """
        This function gets all the pitches from the rules.
        Parameter:
        rule (string): a HON node
        Return
        (list): the list of pitches this rule has.
    """
    if len(rule.split('|')) <= 1:
        return None
    current_node = rule.split('|')[0]
    previous_nodes = rule.split('|')[1].split('.')

    if previous_nodes == ['']:
        pitches = [int(current_node)]
    else:
        pitches = [int(current_node)] + list(map(int, previous_nodes))
    pitches = list(filter(lambda x: x < 128, pitches))
    return pitches


def getAbruptness(graph):
    """
    This function calculates abruptness.
    1) Calculate betweeness/prob for each edge
    2) Get the edge with the highest betweenness/prob score
    3) Calculate pitch difference from the two end node of this edge
    Parameter:
    graph(nx.Digraph): the HON network
    Return:
    (int): the pitch difference
    """
    # calculate betweenness/prob for each edge
    edge_betweeness = nx.edge_betweenness_centrality(
        graph, weight='weight', normalized=True)
    transition_prob = graph.edges(data=True)
    weighted_abruptness = {(e[0], e[1]): 0 for e in transition_prob}
    for edge in transition_prob:
        weighted_abruptness[(edge[0], edge[1])] = edge_betweeness[
            (edge[0], edge[1])] / edge[2]['weight']
    # Get the edge with highest abruptness
    weighted_highest = sorted(
        weighted_abruptness, key=weighted_abruptness.get, reverse=True)[0]
    abruptness = []
    for edge in weighted_highest:
        edge = weighted_highest[0]
        w_rule_1 = edge[0]
        w_rule_2 = edge[1]
        w_pitches_rule1 = getPitchesGivenRules(w_rule_1)
        w_pitches_rule2 = getPitchesGivenRules(w_rule_2)
        if w_pitches_rule1 is None or w_pitches_rule2 is None or len(w_pitches_rule1) == 0 or len(w_pitches_rule2) == 0:
            continue
        pitch_difference = max(abs(max(w_pitches_rule1) - min(w_pitches_rule2)),
                               abs(max(w_pitches_rule2) - min(w_pitches_rule1)))
        abruptness.append(pitch_difference)
        break  # only calculate the one with highest weight
    if len(abruptness) > 0:
        return max(abruptness)
    return 0


def getBranching(graph, tau=0.1):
    """
    This function calculate branching.
    1) filter out edges based on the transition probability threshold tau.
    2) Calculate unweighted mean outdegree of the filtered graph.
    Parameter:
    graph (nx.graph): the network
    tau (float): the threshold to filter the edges
    Return:
    (float): the branching score
    """
    # Edges with weight greater than tau
    edges = [(e[0], e[1])
             for e in graph.edges(data=True) if e[2]['weight'] > tau]
    # Create filtered graph
    sg = nx.DiGraph()
    sg.add_edges_from(edges)
    sg.add_nodes_from(graph.nodes())
    # Calculate mean out degree
    out_degree = [d[1] for d in sg.out_degree()]
    if len(out_degree) > 0:
        return np.mean(out_degree)
    return 0


def getRepeatedness(graph, tau=0.75):
    """
    Calculate repeatedness of the graph.
    1) Filter out edges based on transition threshold
    2) Get the path with the longest length (weighted) and return its length
    Parameter:
    graph (nx.graph): the network
    tau (float): the threshold to filter the edges
    Return:
    (float): the maximum path length (weighted)
    """
    # filter out the edges based threshold
    edges = [(e[0], e[1])
             for e in graph.edges(data=True) if e[2]['weight'] > tau]
    # create filtered graph
    edge_weight = nx.get_edge_attributes(graph, "weight")
    sg = nx.DiGraph()
    sg.add_edges_from(edges)
    nx.set_edge_attributes(sg, edge_weight, "weight")
    # get the path_dict for each path, and record the maximum value
    edge_weight = nx.get_edge_attributes(sg, "weight")
    node_pairs = permutations(list(sg.nodes()), 2)
    path_dict, max_length = {}, 0
    for (n1, n2) in node_pairs:
        paths = list(nx.all_simple_paths(sg, source=n1, target=n2))
        for each_path in paths:
            if len(each_path) > max_length:
                max_length = len(each_path)
            edges = zip(each_path[:-1], each_path[1:])
            prob = sum([edge_weight[edge] for edge in edges])
            path_dict[','.join(each_path)] = prob
    return max_length


def getMelodic(graph):
    """
    Calcualte melodic score. The average of the length of the rule.
    Parameter:
    graph (nx.graph): the network
    (float): the melodic score
    """
    nodes = list(graph.nodes())
    rule_length_list = []
    for node in nodes:
        previous_nodes = node.split('|')[1].split('.')
        if previous_nodes == ['']:
            length = 1
        else:
            length = len(previous_nodes) + 1
        rule_length_list.append(length)

    if len(rule_length_list) > 0:
        return np.mean(rule_length_list)
    return 0


def getPitchRange(graph):
    """
    Get pitch range of the piece and in rules.
    For the range of piece, simply take the maximum and minimum and calculate the difference.
    For the rules, calculate pitch range for each rule and then take the mean.
    Parameter:
    graph (nx.graph): the network
    (float, float): mean pitch range in rules, pitch range of the piece
    """
    nodes = list(graph.nodes())
    pitch_in_rules = []
    for node in nodes:
        pitches = getPitchesGivenRules(node)
        if len(pitches) > 0:
            pitch_in_rules.append(pitches)
    pitch_range_in_rules = []
    for pitches in pitch_in_rules:
        pitch_range_in_rules.append(max(pitches) - min(pitches))
    pitches_in_piece = list(itertools.chain(*pitch_in_rules))
    pitches_in_piece = list(filter(lambda x: x < 128, pitches_in_piece))
    pitches_in_piece = sorted(pitches_in_piece, reverse=True)
    pitch_range_of_piece = max(pitches_in_piece) - min(pitches_in_piece)
    if len(pitch_range_in_rules) > 0:
        return np.mean(pitch_range_in_rules), pitch_range_of_piece
    return 0, pitch_range_of_piece


def getPitchChangeBetweenRules(graph, tau=0.75):
    """
    Get pitch change between rules. Given an edge, calculate largest pitch difference involving to the two end notes. Take the mean of all the edges.
    Parameter:
    graph (nx.graph): the network
    tau (float): the threshold to filter the edges
    Return:
    (float): pitch change between rules
    """
    edges = [(e[0], e[1])
             for e in graph.edges(data=True) if e[2]['weight'] > tau]
    edge_weight = nx.get_edge_attributes(graph, "weight")
    sg = nx.DiGraph()
    sg.add_edges_from(edges)
    nx.set_edge_attributes(sg, edge_weight, "weight")
    pitch_difference_between_rules = []
    for edge in sg.edges():
        rule_1 = edge[0]
        rule_2 = edge[1]
        pitches_rule1 = getPitchesGivenRules(rule_1)
        pitches_rule2 = getPitchesGivenRules(rule_2)
        try:
            pitch_difference = max(abs(max(pitches_rule1) - min(pitches_rule2)),
                                   abs(max(pitches_rule2) - min(pitches_rule1)))
            pitch_difference_between_rules.append(pitch_difference)
        except:
            continue

    if len(pitch_difference_between_rules) > 0:
        return np.mean(pitch_difference_between_rules)
    return 0


def generateFeatures(graph, label):
    """
    The function to generate features for a given graph.
    Parameter
    graph (nx.graph): the network of this piece
    label (string): the genre of this piece
    """
    print('Generating HON Features')
    stime = time.process_time()
    abruptness = getAbruptness(graph)
    branching = getBranching(graph, 0.10)
    repeatedness = getRepeatedness(graph, 0.75)
    melodic = getMelodic(graph)
    pitch_range_rule, pitch_range_piece = getPitchRange(graph)
    pitch_change = getPitchChangeBetweenRules(graph, 0.75)
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    largest_cc = max(nx.connected_components(graph.to_undirected()), key=len)
    diameter = nx.diameter(graph.subgraph(largest_cc).to_undirected())
    avg_shortest_path_length = nx.average_shortest_path_length(graph)
    density = nx.density(graph)
    clustering = nx.average_clustering(graph)
    modularity = community.modularity(community.best_partition(
        graph.to_undirected()), graph.to_undirected())
    data = [abruptness,
            branching,
            repeatedness,
            melodic,
            pitch_range_rule,
            pitch_range_piece,
            pitch_change,
            num_nodes,
            num_edges,
            diameter,
            avg_shortest_path_length,
            density,
            clustering,
            modularity]
    t = time.process_time() - stime
    return data, t
