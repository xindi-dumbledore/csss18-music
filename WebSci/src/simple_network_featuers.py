import csv
import community
import sys
import networkx as nx
import os
import numpy as np
import generate_features as honfeatures


def getFiles(dirname, musictype):
	fnames = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
	fnames = [f for f in fnames if f.startswith(musictype)]
	return fnames


def trajectoryToGraph(fname):
	trajectory = []
	with open(fname, 'r') as f:
		reader = csv.reader(f, delimiter=' ')
		for row in reader:
			trajectory += row

	graph = nx.DiGraph()
	edges = []
	for i in range(1, len(trajectory)-1):
		edge = (trajectory[i], trajectory[i+1])
		
		if not graph.has_edge(edge[0], edge[1]):
			graph.add_edge(edge[0], edge[1], weight=0)

		graph[edge[0]][edge[1]]['weight'] += 1
		#edges.append((trajectory[i], trajectory[i+1]))

	
	# Convert weights to probabilities
	
	for u in graph.nodes():
		m = sum([graph[u][v]['weight'] for v in graph[u]])
		for v in graph[u]:
			graph[u][v]['weight'] = graph[u][v]['weight'] / m
	
	return graph


def getFeatures(graph):
	d1 = graph.number_of_nodes()
	d2 = graph.number_of_edges()

	sg = max(nx.strongly_connected_components(graph), key=len)
	sg = graph.subgraph(sg)

	d3 = nx.diameter(sg)
	d4 = nx.average_shortest_path_length(sg)
	d5 = nx.density(graph)
	d6 = nx.average_clustering(graph)
	d7 = nx.betweenness_centrality(sg)

	edges = list(graph.edges())
	ug = nx.Graph()
	ug.add_edges_from(edges)

	d8 = community.modularity(community.best_partition(ug), ug)

	#print(d7.values())

	return [d1, d2, d3, d4, d5, d6, np.mean(list(d7.values())), d8]

def saveFeatures(sname, feature):
	with open(sname, 'a+') as f:
		writer = csv.writer(f, delimiter='\t')
		for row in features:
			writer.writerow(row)


if __name__ == '__main__':
	tdir = sys.argv[1]
	sname = sys.argv[2]
	mtype = sys.argv[3]
	mlabel = sys.argv[4]

	features = []

	fnames = getFiles(tdir, mtype)

	for f in fnames:
		print('Processing: {}'.format(f))

		f = os.path.join(tdir, f)
		graph = trajectoryToGraph(f)
		
		# Simple network features
		fea = getFeatures(graph)

		# MusicHON Features
		fea += honfeatures.generateFeatures(graph)
		
		fea += [mlabel]
		features.append(fea)

		if len(features) >= 100:
			saveFeatures(sname, features)
			features = []
