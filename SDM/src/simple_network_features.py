import csv
import community
import sys
import networkx as nx
import os
import numpy as np
import generate_features as honfeatures
import generate_gml as gml


def getFiles(dirname, musictype):
	fnames = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
	#fnames = [f for f in fnames if f.endswith('-network.csv')]
	fnames = [f for f in fnames if f.startswith(musictype)]
	return fnames


def trajectoryToGraph(fname, dirname):
	edges = []
	with open(os.path.join(dirname, fname), 'r') as f:
		reader = csv.reader(f, delimiter=' ')
		for row in reader:
			row = row[1:]
			edges += [(row[i], row[i+1]) for i in range(0, len(row)-1)]

	counts = {}
	for e in edges:
		if e[0] not in counts:
			counts[e[0]] = {}
		if e[1] not in counts[e[0]]:
			counts[e[0]][e[1]] = 0
		counts[e[0]][e[1]] += 1

	# Normalize
	edges = []
	for i in counts:
		s = sum(counts[i].values())
		for j in counts[i]:
			edges.append((i,j, counts[i][j]/s))

	#print(edges)
	graph = nx.DiGraph()
	graph.add_weighted_edges_from(edges)

	#print(nx.info(graph))
	return graph


def getFeatures(graph):
	d1 = graph.number_of_nodes()
	d2 = graph.number_of_edges()

	sg = nx.strongly_connected_components(graph)
	sg = [graph.subgraph(c) for c in sg]

	d3 = np.mean([nx.diameter(s) for s in sg])
	d4 = np.mean([nx.average_shortest_path_length(s) for s in sg])
	d5 = nx.density(graph)
	d6 = nx.average_clustering(graph)
	#d7 = nx.betweenness_centrality(sg)

	#edges = list(graph.edges())
	#ug = nx.Graph()
	#ug.add_edges_from(edges)

	#d8 = community.modularity(community.best_partition(ug), ug)

	#print(d7.values())

	return [d1, d2, d3, d4, d5, d6]


def saveFeatures(sname, features):
	with open(sname, 'a+') as f:
		writer = csv.writer(f, delimiter='\t')
		for row in features:
			writer.writerow(row)



def convertToSimpleNetwork(edges):
	simple_edges = []
	for e in edges:
		u = e[0].split('|')[0]
		v = e[1].split('|')[0]
		simple_edges.append((u,v))

	g = nx.DiGraph()
	g.add_edges_from(simple_edges)
	return g


if __name__ == '__main__':
	input_dirname = sys.argv[1]
	#featurefile = sys.argv[2]
	sname = sys.argv[2]
	
	labels = [('pop','POP'),('metal','ROCK'),('classical','CLASSICAL'),('jazz','JAZZ'),('american','FOLK')]

	for m in labels:
		musictype = m[0]
		musiclabel = m[1]

		fnames = getFiles(input_dirname, musictype)

		for f in fnames:
			graph = trajectoryToGraph(f, input_dirname)

			# Simple network features
			features = getFeatures(graph)

			# HON features
			d9 = honfeatures.getAbruptness(graph, None)
			d10 = honfeatures.getBranchisess(graph, 0.1)
			d11, _= honfeatures.getRepeatedness(graph, 0.75)

			features += [d9, d10, d11, musiclabel, f]


			#edges = gml.getEdges(f, input_dirname)

			#graph = convertToSimpleNetwork(edges)

			#print(f)
			#print(nx.info(graph))

			#fea = getFeatures(graph)
			
			#d = np.mean([d[1] for d in graph.out_degree()])
 
			#fea += [d, musiclabel]
			#print(fea)
			saveFeatures(sname, [features])

	"""
	features = []

	fnames = getFiles(tdir, mtype)[:500]

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
	"""