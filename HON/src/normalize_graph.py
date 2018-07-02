import networkx as nx
import sys
import os

def getFileName(dirname):
    fnames = [f for f in os.listdir(
        dirname) if os.path.isfile(os.path.join(dirname, f))]
    fnames = [f for f in fnames if f.endswith('network.csv')]
    return fnames

def readGraph(fname):
	return nx.read_weighted_edgelist(fname)

def normalizeEdgeWeight(graph):
	edge = []
	node_weight = {}
	for e in graph.edges(data=True):
		if e[0] not in node_weight:
			node_weight[e[0]] = 0
		node_weight[e[0]] += e[2]['weight']

	for e in graph.edges(data=True):
		edge.append([e[0], e[1], e[2]['weight']/node_weight[e[0]]])

	graph = nx.DiGraph()
	graph.add_weighted_edges_from(edge)

	return graph

def saveNetwork(graph, sname):
	nx.write_edgelist(graph, sname, data=['weight'])

if __name__ == '__main__':
	inputDir = sys.argv[1]

	for f in getFileName(inputDir):
		fname = os.path.join(inputDir, f)
		print('Files: {}'.format(fname))
		g = readGraph(fname)
		g = normalizeEdgeWeight(g)
		saveNetwork(g, fname)