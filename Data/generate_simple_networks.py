import pickle
import json
import networkx as nx

fname = 'Data/midi_corpus_pop0.json'
sname = 'Data/Simple Network Case Studies/'

with open(fname, 'r') as f:
	midi_corpus = json.load(f)

songs = ["Beatles beatles-yesterday", "Beatles Beatles_Blackbird", "Beatles Beatles_Eleanor_Rigby"]


for each_piece in songs:

#for each_piece in midi_corpus:
	from collections import Counter
	for each_part in midi_corpus[each_piece][1]:
		edges = []
		sequence = midi_corpus[each_piece][1][each_part]
		sequence = [item if type(item)!=list else max(item) for item in sequence]
		edges = list(zip(sequence[:-1], sequence[1:]))
		edges_with_weight = dict(Counter(edges))
		edges_with_weight = [(e[0], e[1], edges_with_weight[e]) for e in edges_with_weight]
		#pickle.dump(edges_with_weight, open("Simple Network/%s %s.pickle"%(each_piece.replace('/',' '), each_part), "wb"))

		print(edges_with_weight)
		graph = nx.DiGraph()
		graph.add_weighted_edges_from(edges_with_weight)

		nx.write_gml(graph, "{}-{}{}".format(sname, each_piece, '.gml'))