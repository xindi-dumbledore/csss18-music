"""
Draw the HON
"""

import sys
import os
import csv
import networkx as nx
import matplotlib.pyplot as plt

def getFiles(dirname):
	fnames = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
	fnames = [f for f in fnames if f.endswith('-network.csv')]
	return fnames

def getEdges(fname, dirname):
	edges = []
	with open(os.path.join(dirname, fname), 'r') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			edges.append((row[0], row[1], float(row[2])))
	return edges

def generateGraph(edges):
	g = nx.DiGraph()
	g.add_weighted_edges_from(edges)
	return g


def nodeSize(graph):
	# Node size by pagerank
	pr = nx.pagerank_numpy(graph, weight='weight')
	max_size = 100
	min_size = 1

	max_pr = max(pr.values())
	min_pr = min(pr.values())

	return [max(min_size, pr[u]/max_pr * max_size) for u in graph.nodes()]

	#return [data[u] for u in graph.nodes()]

def edgeSize(graph):
	# Edge size by weight
	esize = [e[2]['weight'] for e in graph.edges(data=True)]
	mesize = max(esize)
	return [e/mesize for e in esize]


def drawGraph(graph, dirname, fname):
	nsize = nodeSize(graph)
	esize = edgeSize(graph)

	f = '{}{}'.format(fname[:-3], 'pdf')
	sname = os.path.join(dirname, f )

	nx.draw(graph, arrowsize=5, arrows=True, arrowstyle='-|>', node_size=nsize, width=esize, edge_color='gray', node_color='red', with_labels=True, font_size=5)
	plt.figure(1,figsize=(20,20)) 
	plt.savefig(sname, bbox_inches='tight', dpi=1000)
	plt.clf()


def saveGML(graph, dirname, fname):
	f = '{}{}'.format(fname[:-3], 'gml')
	sname = os.path.join(dirname, f )

	nx.write_gml(graph, sname)


if __name__ == '__main__':
	input_dirname = sys.argv[1]
	output_dirname = sys.argv[2]
	gml_dirname = sys.argv[3]

	fnames = getFiles(input_dirname)

	for f in fnames:
		print('Processing: \t {}'.format(f))
		edges = getEdges(f, input_dirname)
		if len(edges) == 0:
			continue
		graph = generateGraph(edges)
		#drawGraph(graph, output_dirname, f)
		saveGML(graph, gml_dirname, f)



