"""
Compare some given trajectories to some HON and output which one it most likely came from
"""

import csv
import numpy as np
import sys
import hon

epsilon = np.log(0.00000001)

def get_model(edges):
	adj = {}
	for e in edges:
		d = edges[e]
		source = d['last']
		target = e[1]
		path = e[0]

		#print(source, target)

		if source not in adj:
			adj[source] = {}
		if target not in adj[source]:
			adj[source][target] = {}
		adj[source][target][path] = float(d['probability'])
	return adj

def split_train_test(data, ratio=0.9):
	np.random.shuffle(data)

	return data[:int(len(data)*ratio)], data[int(len(data)*ratio) + 1 :]

def get_trajectories(fname):
	traj = []
	with open(fname, 'r') as f:
		for row in f:
			traj.append(row)
	return traj

def get_longest_path_prob(sub_paths, priors):
	l_max = 0
	pr = epsilon
	for p in sub_paths:
		if priors.endswith(p):
			l = len(p.split('>'))
			if l > l_max:
				l_max = l
				pr = sub_paths[p]
				#print(l_max, pr)
	return np.log(pr)

def path_probability(model, trajectory):
	prior = []
	prob = 0
	uncertainty = 0

	for i in range(0, len(trajectory)-1):
		s = trajectory[i]
		t = trajectory[i+1]

		prior.append(s)

		if s in model and t in model[s]:
			p = get_longest_path_prob(model[s][t], '>'.join(prior))
			prob += p
		else:
			#print(s,t)
			prob += epsilon
			uncertainty += 1
		
	return prob, uncertainty/len(trajectory)


def model_comparison(models, trajectory):
	prediction = []
	for t in trajectory:
		p, u = [], []
		for m in models:
			prob, uncertainty = path_probability(m, t)
			p.append(prob)
			u.append(uncertainty)
		#print(p, u)	
		prediction.append(p.index(max(p)))
	return prediction
		#print('Uncertainty', u)


if __name__ == '__main__':
	mname = sys.argv[1:]

	h = hon.HON()

	traj = []
	for f in mname:
		traj.append(get_trajectories(f))

	confusion_matrix = [[0]*len(mname) for _ in range(0, len(mname))]
	#print(confusion_matrix)
	
	for x in range(0, 30):
		print('Iteration: {}'.format(x))
		models, traj_test = [], []

		for t in traj:
			t0, t1 = split_train_test(t)
			#print(len(t0))
			h_edges = h.get_edges(t0, sep='\t', max_prior=5, min_support=5, delta_confidence=0.05)
			m = get_model(h_edges)
			#print(m)
			models.append(m)
			traj_test.append([t.split('\t') for t in t1])

		for i in range(0, len(models)):
			t = traj_test[i]
			pred = model_comparison(models, t)
			for p in pred:
				confusion_matrix[i][p] += 1
		print(confusion_matrix)
