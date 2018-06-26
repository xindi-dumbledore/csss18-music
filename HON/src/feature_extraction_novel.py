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
	fnames = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
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
	unweighted_edge_betweeness = nx.edge_betweenness_centrality(graph, normalized=True)
	weighted_edge_betweeness = nx.edge_betweenness_centrality(graph, normalized=True, weight='weight')
	transition_prob = graph.edges(data=True)

	unweighted_abruptness = {}
	weighted_abruptness = {}

	for edge in transition_prob:
		unweighted_abruptness[(edge[0],edge[1])] = unweighted_edge_betweeness[(edge[0],edge[1])]/edge[2]['weight']
		weighted_abruptness[(edge[0],edge[1])] = weighted_edge_betweeness[(edge[0],edge[1])]/edge[2]['weight']
	
	return unweighted_abruptness.values(), weighted_abruptness.values()

def getBranchisess(graph, tau=0.1):
	"""
	Unweighted out-degree counting only edges with weight greater than tau
	"""

	# Edges with weight greater than tau
	edges = [(e[0],e[1]) for e in graph.edges(data=True) if e[2]['weight'] > tau]
	
	sg = nx.Graph()
	sg.add_edges_from(edges)
	sg.add_nodes_from(graph.nodes()) 			# add nodes in case there are nodes which are not included in edges
	
	degree = nx.degree(sg)
	return [d[1] for d in degree]


def getRepeatedness(graph, tau=0.75):
	"""
	Unweighted chaings of edge weight greather than tau
	"""
	edges = [(e[0],e[1]) for e in graph.edges(data=True) if e[2]['weight'] > tau]

	sg = nx.Graph()
	sg.add_edges_from(edges)
	

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

		#print(d0)
		#data['unweighted_abruptness'] += d0
		#print(data['unweighted_abruptness'])
		#data['weighted_abruptness'] += d1
		#data['branchiness'] += d2

		data['unweighted_abruptness'].append(np.percentile(d0,95))
		data['weighted_abruptness'].append(np.percentile(d1,95))
		data['branchiness'].append(np.mean(d2))

	saveData(sname, data)