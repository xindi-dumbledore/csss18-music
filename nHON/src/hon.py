"""
Creates HON from trajectories
One line in the input file is considered one trajectory
"""

import sys
import csv

class HON(object):
	"""docstring for HON"""
	def __init__(self):
		super(HON, self).__init__()


	def read_trajectory(self, fname):
		data = []
		with open(fname, 'r') as file:
			for row in file:
				data.append(row)
		return data

	def get_edges(self, trajectory, delta_confidence=0.05, min_support=10, sep='\t', max_prior=-1):
		"""
		Reads the input trajectory file and construct the HON
		Inputs:
			fname : The file name of the trajectory
			confidence: The minimum confidence required to include a rule (path)
			support: The minimum number of times the rule (path) is observed to consider it for HON
			seperator: The node separator in trajectory file
			max_prior: The maximum order to consider (-1 is unlimited) (Increasing this number slows down algorithm.)
		"""
		paths = {}
		
		#with open(fname, 'r') as file:
		lnum = 0
		for line in trajectory:
			lnum += 1
			line = line.rstrip('\n')
			nodes = line.split(sep)
			if len(nodes) < 2:
				continue

			for i in range(0, len(nodes)-1):
				target = nodes[i + 1]
					
				if max_prior == -1:
					k = 0
				else:
					k = max(0, i - max_prior)

				for j in range(k, i):
					source = tuple(nodes[j:i])
					#print(source, target)

					if source not in paths:
						paths[source] = {}

					if target not in paths[source]:
						paths[source][target] = {'confidence':0, 'support':0}

					paths[source][target]['support'] += 1
			#print('Line # {}'.format(lnum))

		# Remove paths with less than min_support
		for source in paths:
			remove = []
			path_sum = 0

			for target in paths[source]:
				if paths[source][target]['support'] < min_support:
					remove.append(target)

				path_sum += paths[source][target]['support']

			for target in paths[source]:
				paths[source][target]['confidence'] = paths[source][target]['support']/path_sum


		# Remove paths with low confidence delta
		# If the confidence does not imporve by at least delta_confidence by adding one more order, dont add the higher order
		for source in paths:
			if len(source) == 1:
				continue

			# Confidence from lower orders
			remove = []
			p_source = source[1:]

			if p_source not in paths:
				continue

			for target in paths[source]:
				p_confidence = max([paths[source[i:]][target]['confidence'] for i in range(1, len(source)) if source[i:] in paths and target in paths[source[i:]]])
				if abs(paths[source][target]['confidence'] - p_confidence) < delta_confidence:
					remove.append(target)

			for target in remove:
				del paths[source][target]


		# Remove paths with no targets
		remove = []
		for source in paths:
			if len(paths[source]) == 0:
				remove.append(source)

		for source in remove:
			del paths[source]


		# Reformat the edges to adjaceny lists
		adjaceny_list = {}
		for source in paths:
			for target in paths[source]:
				s = '>'.join(source)
				t = target
				p = source[-1]
				
				if s not in adjaceny_list:
					adjaceny_list[s] = {}

				adjaceny_list[s][t] = {'last':p, 'confidence': paths[source][target]['confidence'], 'support': paths[source][target]['support']}

		# Add transition probability and convert to edges
		edges = {}
		for s in adjaceny_list:
			wt = sum([adjaceny_list[s][t]['support'] for t in adjaceny_list[s] if adjaceny_list[s][t]['support'] > 0])
			if wt == 0:
				continue
			for t in adjaceny_list[s]:
				adjaceny_list[s][t]['probability'] = adjaceny_list[s][t]['support']/wt
				if adjaceny_list[s][t]['support'] > 0:
					edges[(s,t)] = adjaceny_list[s][t]
		
		return edges


	def save_edges(self, edges, sname, delim='\t'):
		"""
		Write the HON edgelist to a file
		"""
		with open(sname, 'w') as f:
			writer = csv.writer(f, delimiter=delim)
			writer.writerow(['Path', 'Target', 'Source', 'Support', 'Confidence', 'Probability'])

			for e in edges:
				#for d in edges[e]:
				d = edges[e]
				writer.writerow([e[0], e[1], d['last'], d['support'], d['confidence'], d['probability']])

	
	def generate_network(self, edges):
		graph = {}
		d = edges[e]

		for e in edges:
			if d['last'] not in graph:
				graph[d['last']] = {}
			if e[1] not in graph[d['last']]:
				graph[d['last']][e[1]] = {}
			
			graph[e[0]][e[1]][d['']]


	## Todo generate graph, pagerank, degree, centralities etc.

		

if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]

	h = HON()
	traj = h.read_trajectory(fname)
	edges = h.get_edges(traj, sep='\t', max_prior=10, min_support=1, delta_confidence=0.05)
	h.save_edges(edges, sname)