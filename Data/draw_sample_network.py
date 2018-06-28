from __future__ import division

import networkx as nx
import os
import sys
import matplotlib.pyplot as plt

def readGML(gname):
	graph = nx.read_gml(gname)
	return graph

def drawGraph(graph, dirname, fname):
	nsize = nodeSize(graph)
	esize = edgeSize(graph)

	#print(esize)

	f = '{}{}'.format(fname[:-3], 'pdf')
	sname = os.path.join(dirname, f )

	nx.draw(graph, arrowsize=5, arrows=True, arrowstyle='-|>', node_size=nsize, width=esize, edge_color='gray', node_color='red', with_labels=True, font_size=5)
	plt.figure(1,figsize=(20,20)) 
	plt.savefig(sname, bbox_inches='tight', dpi=1000)
	plt.clf()

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

def getFiles(dirname):
	fnames = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
	#fnames = [f for f in fnames if f.endswith('-network.csv')]
	return fnames

if __name__ == '__main__':
	input_dirname = sys.argv[1]
	output_dirname = sys.argv[2]

	fnames = getFiles(input_dirname)

	for f in fnames:
		fname = os.path.join(input_dirname, f)
		print('Processing: \t {}'.format(f))
		graph = readGML(fname)
		drawGraph(graph, output_dirname, f)