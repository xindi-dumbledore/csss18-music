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
import operator
import community
from itertools import permutations
import itertools
from scipy.stats import wasserstein_distance
import time
from scipy.stats import skew

# ----- Part to set timeout if something takes too long
import signal

class TimeoutException(Exception):   # Custom exception class
	pass

def timeout_handler(signum, frame):   # Custom signal handler
	raise TimeoutException

# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)
# ---- Part to set timeout if something takes too long


def getFileName(dirname, musictype):
	fnames = [f for f in os.listdir(
		dirname) if os.path.isfile(os.path.join(dirname, f))]
	fnames = [f for f in fnames if f.startswith(musictype)]
	return fnames


def getGMLNetwork(fname):
	"""
	Read the network stored as GML
	"""
	graph = nx.read_gml(fname)
	rnodes = [u for u in graph.nodes() if '|' not in u]
	graph.remove_nodes_from(rnodes)
	return graph


def getPitchOffset(graph):
	# this function is currently incorrect
	rpitch = set([int(u.split('|')[0]) for u in graph.nodes()])
	return -1 * min(rpitch)


def getFrequency(note):
	#return note
	fmap = {0: 8.18, 1: 8.666408111859035, 2: 9.18173955517067, 3: 9.727714200722259, 4: 10.306154188140065, 5: 10.918990007110883, 6: 11.56826694021192, 7: 12.256151888851258, 8: 12.984940605099876, 9: 13.757065353550773, 10: 14.575103028775958, 11: 15.441783755472512, 12: 16.360000000000007, 13: 17.332816223718076, 14: 18.363479110341352, 15: 19.45542840144453, 16: 20.61230837628014, 17: 21.837980014221777, 18: 23.13653388042385, 19: 24.512303777702527, 20: 25.969881210199766, 21: 27.514130707101565, 22: 29.15020605755193, 23: 30.88356751094504, 24: 32.720000000000034, 25: 34.66563244743618, 26: 36.72695822068272, 27: 38.91085680288907, 28: 41.2246167525603, 29: 43.675960028443576, 30: 46.27306776084773, 31: 49.02460755540508, 32: 51.93976242039955, 33: 55.02826141420316, 34: 58.30041211510389, 35: 61.76713502189011, 36: 65.4400000000001, 37: 69.33126489487239, 38: 73.45391644136548, 39: 77.82171360577819, 40: 82.44923350512065, 41: 87.35192005688721, 42: 92.5461355216955, 43: 98.04921511081021, 44: 103.87952484079916, 45: 110.05652282840637, 46: 116.60082423020783, 47: 123.5342700437803, 48: 130.88000000000025, 49: 138.66252978974487, 50: 146.90783288273104, 51: 155.64342721155649, 52: 164.89846701024135, 53: 174.7038401137745, 54: 185.0922710433911, 55: 196.09843022162053, 56: 207.75904968159844, 57: 220.11304565681286, 58: 233.20164846041578, 59: 247.0685400875607, 60: 261.7600000000007, 61: 277.32505957948985, 62: 293.8156657654622, 63: 311.28685442311314, 64: 329.79693402048287, 65: 349.4076802275492, 66: 370.1845420867824, 67: 392.19686044324123, 68: 415.51809936319705, 69: 440.22609131362594, 70: 466.4032969208318, 71: 494.1370801751217, 72: 523.5200000000016, 73: 554.65011915898, 74: 587.6313315309249, 75: 622.5737088462265, 76: 659.5938680409661, 77: 698.8153604550987, 78: 740.3690841735652, 79: 784.3937208864829, 80: 831.0361987263946, 81: 880.4521826272523, 82: 932.806593841664, 83: 988.2741603502438, 84: 1047.0400000000036, 85: 1109.3002383179605, 86: 1175.2626630618502, 87: 1245.1474176924537, 88: 1319.1877360819328, 89: 1397.630720910198, 90: 1480.738168347131, 91: 1568.7874417729665, 92: 1662.0723974527903, 93: 1760.9043652545054, 94: 1865.6131876833292, 95: 1976.5483207004886, 96: 2094.080000000008, 97: 2218.6004766359224, 98: 2350.5253261237017, 99: 2490.2948353849088, 100: 2638.375472163867, 101: 2795.2614418203975, 102: 2961.4763366942634, 103: 3137.574883545935, 104: 3324.144794905582, 105: 3521.8087305090125, 106: 3731.2263753666602, 107: 3953.0966414009795, 108: 4188.160000000019, 109: 4437.200953271847, 110: 4701.050652247406, 111: 4980.58967076982, 112: 5276.750944327737, 113: 5590.522883640798, 114: 5922.9526733885305, 115: 6275.149767091873, 116: 6648.289589811167, 117: 7043.617461018029, 118: 7462.452750733324, 119: 7906.193282801963, 120: 8376.320000000043, 121: 8874.401906543697, 122: 9402.101304494816, 123: 9961.179341539644, 124: 10553.501888655479, 125: 11181.045767281601, 126: 11845.905346777066, 127: 12550.299534183754}
	return fmap[note]


def getEqualCountourWeight(freq):
	weight = {20.0: 0.03495714930085714, 25.0: 0.15820929183581411, 31.5: 0.27661253946774933, 40.0: 0.3847541723049166, 50.0: 0.4738385205232296, 63.0: 0.5501804239963916, 80.0: 0.6160351826792965, 100.0: 0.6668921966621562, 125.0: 0.7104194857916103, 160.0: 0.7502255299954894, 200.0: 0.7843933243121336, 250.0: 0.813148398737032, 315.0: 0.8405502931889941, 400.0: 0.8636671177266577, 500.0: 0.8814839873703203, 630.0: 0.8947902571041949, 800.0: 0.9015561569688769, 1000.0: 0.8982859720342806, 1250.0: 0.8865584122688318, 1600.0: 0.9115922417681552, 2000.0: 0.9445196211096076, 2500.0: 0.9776725304465494, 3150.0: 1.0, 4000.0: 0.9939106901217862, 5000.0: 0.9486919260261615, 6300.0: 0.8611862877762743, 8000.0: 0.7873252142534958, 10000.0: 0.7799954894000902, 12500.0: 0.8036761389264773, 16000.0: 0.7391745602165088, 20000.0: 0.0}
	ref_freq = np.array([20.0, 25.0, 31.5, 40.0, 50.0, 63.0, 80.0, 100.0, 125.0, 160.0, 200.0, 250.0, 315.0, 400.0, 500.0, 630.0, 800.0, 1000.0, 1250.0, 1600.0, 2000.0, 2500.0, 3150.0, 4000.0, 5000.0, 6300.0, 8000.0, 10000.0, 12500.0, 16000.0, 20000.0])

	cf = ref_freq[np.abs(ref_freq - freq).argmin()]

	return weight[cf]


def getPitchesGivenRules(rule):
	# this is a helper function
	# Get the pitches based on the rules
	if len(rule.split('|')) <= 1:
		return None
	current_node = rule.split('|')[0]
	#print(rule, current_node, rule.split('|'))
	previous_nodes = rule.split('|')[1].split('.')
	
	if previous_nodes == ['']:
		pitches = [int(current_node)]
	else:
		pitches = [int(current_node)] + list(map(int, previous_nodes))
	pitches = list(filter(lambda x: x < 128, pitches))
	return pitches


def getAbruptness(graph, label):
	"""
	Edges with high betweeness but low transition prob

	Defined as betweenss/prob
	"""

	pitch = getPitchOffset(graph)
	#d = int(np.sqrt(graph.number_of_nodes()))
	#u_node_betweeness = nx.betweenness_centrality(graph, k=d)
	edge_betweeness = nx.edge_betweenness_centrality(graph, weight='weight', normalized=True)

	transition_prob = graph.edges(data=True)

	weighted_abruptness = {(e[0],e[1]):0 for e in transition_prob}

	for edge in transition_prob:
		weighted_abruptness[(edge[0], edge[1])] = edge_betweeness[(edge[0], edge[1])]/edge[2]['weight']

	# Get edge highest abruptness
	weighted_highest = sorted(weighted_abruptness, key=weighted_abruptness.get, reverse=True)
	#weighted_highest = [weighted_highest]

	abruptness0 = []
	abruptness1 = []	
	for edge in weighted_highest:
		w_rule_1 = edge[0]
		w_rule_2 = edge[1]
		w_pitches_rule1 = getPitchesGivenRules(w_rule_1)
		w_pitches_rule2 = getPitchesGivenRules(w_rule_2)

		#print(w_pitches_rule1, w_pitches_rule2)

		if w_pitches_rule1 is None or w_pitches_rule2 is None or len(w_pitches_rule1) == 0 or len(w_pitches_rule2) == 0 :
			continue

		#freq1 = [getFrequency(n + pitch) for n in w_pitches_rule1]
		#freq2 = [getFrequency(n + pitch) for n in w_pitches_rule2]

		#eqWeight = [getEqualCountourWeight(f) for f in freq1]
		#eqWeight += [getEqualCountourWeight(f) for f in freq2]
		#eqWeight = max(eqWeight)
		#eqWeight = 1.0

		#print(freq1, freq2, [p + pitch for p in w_pitches_rule1], [p + pitch for p in w_pitches_rule2], eqWeight)

		#freq_difference = max( abs(max(freq1) - min(freq2)),
		#					abs(max(freq2) - min(freq1)))

		pitch_difference = max( abs(max(w_pitches_rule1) - min(w_pitches_rule2)),
								abs(max(w_pitches_rule2) - min(w_pitches_rule1)))

		#abruptness0.append(eqWeight * freq_difference)
		abruptness1.append(pitch_difference)

		break

	if len(abruptness1) > 0:
		return max(abruptness1)

	return 0
	#v = max(abruptness0)
	#print(abruptness1)
	#return max(abruptness1)


def getPitchAsymetry(graph, label):
	"""
	Difference between the freq differences between inter and intra community edges
	"""

	pitch = getPitchOffset(graph)

	partition = community.best_partition(graph.to_undirected())
	modularity = community.modularity(partition, graph.to_undirected())

	com = {}
	for u in partition:
		if partition[u] not in com:
			com[partition[u]] = set([])
		com[partition[u]].update([u])

	# Find edges between communities
	inter_edges = set(graph.edges(data=False))
	intra_edges = set([])
	for i in com:
		sg = graph.subgraph(com[i])
		edges = sg.edges(data=False)
		inter_edges.difference_update(edges)
		intra_edges.update(edges)

	baseline0 = []
	for edge in intra_edges:

		w_rule_1 = edge[0]
		w_rule_2 = edge[1]
		
		w_pitches_rule1 = getPitchesGivenRules(w_rule_1)
		w_pitches_rule2 = getPitchesGivenRules(w_rule_2)

		if w_pitches_rule1 is None or w_pitches_rule2 is None or len(w_pitches_rule1) == 0 or len(w_pitches_rule2) == 0:
			continue

		freq1 = [getFrequency(n + pitch) for n in w_pitches_rule1]
		freq2 = [getFrequency(n + pitch) for n in w_pitches_rule2]

		eqWeight = [getEqualCountourWeight(f) for f in freq1]
		eqWeight += [getEqualCountourWeight(f) for f in freq2]
		eqWeight = max(eqWeight)
		eqWeight = 1.0

		freq_difference = max( abs(max(freq1) - min(freq2)),
							abs(max(freq2) - min(freq1)))

		baseline0.append(eqWeight * freq_difference)

	abruptness0 = []	
	for edge in inter_edges:
		w_rule_1 = edge[0]
		w_rule_2 = edge[1]
		w_pitches_rule1 = getPitchesGivenRules(w_rule_1)
		w_pitches_rule2 = getPitchesGivenRules(w_rule_2)

		if w_pitches_rule1 is None or w_pitches_rule2 is None or len(w_pitches_rule1) == 0 or len(w_pitches_rule2) == 0 :
			continue

		freq1 = [getFrequency(n + pitch) for n in w_pitches_rule1]
		freq2 = [getFrequency(n + pitch) for n in w_pitches_rule2]

		eqWeight = [getEqualCountourWeight(f) for f in freq1]
		eqWeight += [getEqualCountourWeight(f) for f in freq2]
		eqWeight = max(eqWeight)
		eqWeight = 1.0

		#print(freq1, freq2, [p + pitch for p in w_pitches_rule1], [p + pitch for p in w_pitches_rule2], eqWeight)

		freq_difference = max( abs(max(freq1) - min(freq2)),
							abs(max(freq2) - min(freq1)))

		abruptness0.append(eqWeight * freq_difference)

	v = wasserstein_distance(abruptness0, baseline0)

	return v, modularity, len(com)


def getBranchisess(graph, tau=0.1):
	"""
	Unweighted out-degree counting only edges with weight greater than tau
	"""
	#m = graph.number_of_nodes() - 1
	# Edges with weight greater than tau
	edges = [(e[0], e[1]) for e in graph.edges(data=True) if e[2]['weight'] > tau]

	sg = nx.DiGraph()
	sg.add_edges_from(edges)
	sg.add_nodes_from(graph.nodes())

	degree0 = [d[1] for d in sg.out_degree()]
	#degree1 = [d[1] for d in sg.degree()]

	if len(degree0) > 0:
		return np.mean(degree0)

	return 0


def estPathLength(graph):
	lengths = []
	edge_weight = nx.get_edge_attributes(graph, "weight")
	pathProb = []

	#print(nx.info(graph))
	# initial prob
	initial_prob = nx.eigenvector_centrality_numpy(graph, weight='weight')
	#initial_prob = {u:1/graph.number_of_nodes() for u in graph.nodes()}

	for u in graph.nodes():
		pathProb.append([[u], u, initial_prob[u], None])
	
	variance, skewness = {}, {}
	l = 0
	while l < 5:
		l += 1
		probs, tprobPaths = [], []
		for path in pathProb:
			if path[0] is None:
				continue

			u = path[1]
			p = path[2]
			
			n = {v:edge_weight[(u,v)] for v in graph.neighbors(u)}
			if len(n) == 0:
				continue
			
			for v in n:
				pr = p * edge_weight[(u,v)]
				probs.append(pr)
				no = path[0] + [v]
				#print(path[0], no)
				tprobPaths.append([no, v, pr, None])
		
		variance[l] = np.var(probs)
		skewness[l] = skew(probs)
		pathProb = tprobPaths
		#print(probs)
		#print(variance, skewness, np.mean(probs), sum(probs), len(probs), len(pathProb))

	return variance[5]


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
	path_dict, max_length = {}, 0
	for (n1, n2) in node_pairs:
		paths = list(nx.all_simple_paths(sg, source=n1, target=n2))
		for each_path in paths:
			if len(each_path) > max_length:
				max_length = len(each_path)

			edges = zip(each_path[:-1], each_path[1:])
			prob = np.prod([edge_weight[edge] for edge in edges])
			path_dict[','.join(each_path)] = prob

	#print(path_dict)
	return max_length, len(path_dict)

	"""
	Unweighted chaings of edge weight greather than tau
	"""
	#return 1
	#threshold = sorted(list(eigen.values()))[int(0.95 * len(eigen))]
	#nodes = set([u for u in eigen if eigen[u] >= threshold])


	sg = graph.copy()
	redges = [(e[0], e[1]) for e in sg.edges(data=True) if e[2]['weight'] <= tau]
	# Remove low prob edges
	sg.remove_edges_from(redges)

	eigen = nx.eigenvector_centrality_numpy(sg, weight='weight')
	nodes = sorted(eigen, key=eigen.get, reverse=True)[:50]

	#cc = [graph.subgraph(c) for c in nx.strongly_connected_components(graph)]
	#dia = max([nx(c) for c in cc])

	return estPathLength(sg, nodes)


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

	if len(rule_length_list) > 0:
		return np.mean(rule_length_list)

	return 0


def getPitchRange(graph):
	#import itertools
	pitch = getPitchOffset(graph)

	nodes = list(graph.nodes())
	pitch_in_rules = []
	for node in nodes:
		pitches = getPitchesGivenRules(node)
		if len(pitches) > 0:
			pitch_in_rules.append(pitches)
	freq_range_in_rules = []
	pitch_range_in_rules = []

	for pitches in pitch_in_rules:
		#freq = [getFrequency(n + pitch) for n in pitches]
		#freq_range_in_rules.append(max(freq) - min(freq))
		pitch_range_in_rules.append(max(pitches) - min(pitches))

	pitches_in_piece = list(itertools.chain(*pitch_in_rules))
	pitches_in_piece = list(filter(lambda x: x < 128, pitches_in_piece))

	#freq_in_piece = sorted([getFrequency(n + pitch) for n in pitches_in_piece], reverse=True)
	pitches_in_piece = sorted(pitches_in_piece, reverse=True)

	#freq_range_of_piece = max(freq_in_piece) - min(freq_in_piece) #np.mean(freq_in_piece[:5]) - np.mean(freq_in_piece[-5:])
	pitch_range_of_piece = max(pitches_in_piece) - min(pitches_in_piece) #np.mean(pitches_in_piece[:5]) - np.mean(pitches_in_piece[-5:])

	if len(pitch_range_in_rules) > 0:
		return np.mean(pitch_range_in_rules), pitch_range_of_piece

	return 0, pitch_range_of_piece


def getPitchChangeBetweenRules(graph, tau=0.75):
	pitch = getPitchOffset(graph)

	edges = [(e[0], e[1])
			 for e in graph.edges(data=True) if e[2]['weight'] > tau]
	edge_weight = nx.get_edge_attributes(graph, "weight")
	sg = nx.DiGraph()
	sg.add_edges_from(edges)
	nx.set_edge_attributes(sg, edge_weight, "weight")
	pitch_difference_between_rules = []
	freq_difference_between_rules = []
	for edge in sg.edges():
		rule_1 = edge[0]
		rule_2 = edge[1]
		pitches_rule1 = getPitchesGivenRules(rule_1)
		pitches_rule2 = getPitchesGivenRules(rule_2)

		#freq1 = [getFrequency(n + pitch) for n in pitches_rule1]
		#freq2 = [getFrequency(n + pitch) for n in pitches_rule2]

		try:
			#freq_difference = max(abs(max(freq1) - min(freq2)),
			#					   abs(max(freq2) - min(freq1)))
			pitch_difference = max(abs(max(pitches_rule1) - min(pitches_rule2)),
								abs(max(pitches_rule2) - min(pitches_rule1)))

			pitch_difference_between_rules.append(pitch_difference)
			#freq_difference_between_rules.append(freq_difference)
		except:
			continue
	
	if len(pitch_difference_between_rules) > 0:
		return np.mean(pitch_difference_between_rules)
	return 0

def saveData(sname, data, mlabel):
	dkeys = data.keys()
	tdata = [dkeys]

	for i in range(0, max([len(data[d]) for d in data])):
		row = [mlabel]

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


def generateFeatures(graph, label):
	#graph = getGMLNetwork(os.path.join(dirname, f))

	print('Generating HON Features')

	stime = time.process_time()

	print(nx.info(graph))
	
	d2 = estPathLength(graph)

	d0 = getAbruptness(graph, label)

	d1  = getBranchisess(graph, 0.10)

	#d2, d7 = getRepeatedness(graph, 0.75)

	d3 = getMelodic(graph)

	d4, d5 = getPitchRange(graph)
	
	d6  = getPitchChangeBetweenRules(graph, 0.75)

	#d12, d13, d14 = getPitchAsymetry(graph, label)

	d8 = graph.number_of_nodes()
	d9 = graph.number_of_edges()

	largest_cc = max(nx.connected_components(graph.to_undirected()), key=len)
	d10 = nx.diameter(graph.subgraph(largest_cc).to_undirected())
	d11 = nx.average_shortest_path_length(graph)
	d12 = nx.density(graph)
	d13 = nx.average_clustering(graph)
	d14 = community.modularity(community.best_partition(graph.to_undirected()), graph.to_undirected())

	data = [d0, d1, d2, d3, d4, d5, d6, 0, d8, d9, d10, d11, d12, d13, d14]

	t = time.process_time() - stime

	return data, t

if __name__ == '__main__':
	dirname = sys.argv[1]			# GML dirname
	sname = sys.argv[2]				# Save file name
	musictype = sys.argv[3] 		# Music Type / Genre
	mlabel = sys.argv[4]

	data = {}
	data['unweighted_abruptness'] = []
	data['weighted_abruptness'] = []
	data['branchiness_mean'] = []
	data['branchiness_variance'] = []
	data['repeteadness_mean'] = []
	data['repeteadness_variance'] = []
	data['melodic_mean'] = []
	data['melodic_variance'] = []
	data['pitch_in_piece'] = []
	data['pitch_in_rules'] = []
	data['pitch_between_rules'] = []

	for f in getFileName(dirname, musictype):
		print('Processing: {}'.format(f))
		generateFeatures(dirname, f, data)

		"""
		try:
			signal.alarm(60)

			# If a particular file takes too long , skip it
			generateFeatures(dirname, f, data)
		except TimeoutException:
			# handle the exception
			signal.alarm(0)
			print('Timeout')
			continue # continue the for loop if function A takes more than 10 second
		else:
			# Reset the alarm
			signal.alarm(0)
		"""

		break

	saveData(sname, data, mlabel)
