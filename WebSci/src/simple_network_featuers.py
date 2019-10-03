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
	fnames = [f for f in fnames if f.endswith('-network.csv')]
	fnames = [f for f in fnames if f.startswith(musictype)]
	return fnames






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
		np.random.shuffle(fnames)
		fnames = fnames[:500]

		for f in fnames:
			edges = gml.getEdges(f, input_dirname)

			graph = convertToSimpleNetwork(edges)

			print(f)
			print(nx.info(graph))

			fea = getFeatures(graph)
			
			d = np.mean([d[1] for d in graph.out_degree()])
 
			fea += [d, musiclabel]
			print(fea)
			saveFeatures(sname, [fea])

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