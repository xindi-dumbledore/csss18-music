import os
import sys
import csv
import numpy as np
import scipy.stats as stats

def getFiles(dirname, musictype):
	fnames = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
	fnames = [f for f in fnames if f.endswith('-rules.csv')]

	if musictype is not 'pop' or musictype is not 'rock':
		fnames = [f for f in fnames if f.startswith(musictype)]
	else:
		fnames = [f for f in fnames if f.startswith('pop') or f.startswith('rock')]

	return fnames


def getFilesArtist(dirname, musictype):
	fnames = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
	fnames = [f for f in fnames if f.endswith('-rules.csv')]

	fnames = [f for f in fnames if musictype in f]
	
	return fnames


def is_digit(n):
	try:
		int(n)
		return True
	except ValueError:
		return  False


def getRules(fname, dirname):
	rules = []
	with open(os.path.join(dirname, fname), 'r') as f:
		reader = csv.reader(f, delimiter=' ')
		for row in reader:
			notes = [int(n) for n in row[:-1] if is_digit(n)]
			m = min(notes)
			notes = [n - m for n in notes]
			prob = float(row[-1])
			rules.append([notes, prob])
	return rules

def filterByLength(rules, minlen=1):
	return [r for r in rules if len(r[0]) > minlen]

def filterBySupport(rules, fcount, minsup=0.25):
	minsup = fcount * minsup
	
	support, psupport = {}, {}
	for r in rules:
		n = tuple(r[0][:-1])
		if n not in support:
			support[n] = 0
			psupport[n] = 0
		support[n] += 1
		psupport[n] += r[1]

	# greater than min sup
	srules = [r for r in support if support[r] >= minsup]
	psupport = {r:psupport[r] for r in srules}
	
	rules = [r for r in rules if tuple(r[0][:-1]) in srules]

	return rules, psupport


def filterByConfidence(rules, support, minconf=0.25):
	confidence = {}
	for r in rules:
		n = tuple(r[0])
		if n not in confidence:
			confidence[n] = 0
		confidence[n] += r[1]

	for r in confidence:
		confidence[r] = confidence[r]/support[tuple(r[:-1])]

	confidence = {r:confidence[r] for r in confidence if confidence[r] >= minconf}
	
	# provide more incentive to longer rules 
	rules = list(confidence.keys())
	rules = sorted(rules, key=lambda x: len(x), reverse=True)
	rules = sorted(rules, key=lambda x: confidence[x], reverse=True)
	
	return rules



def getRelevantRules(input_dirname, musictype):
	#fnames = getFiles(input_dirname, musictype)
	fnames = getFilesArtist(input_dirname, musictype)
	print(len(fnames))

	rules, fcount = [], len(fnames)
	for f in fnames:
		rules += getRules(f, input_dirname)

	rules = filterByLength(rules, 1)
	rules, support = filterBySupport(rules, fcount, 0.25)		
	rules = filterByConfidence(rules, support, 0.75)

	return rules


if __name__ == '__main__':
	input_dirname = sys.argv[1]
	musictype0 = sys.argv[2]
	musictype1 = sys.argv[3]

	rules0 = getRelevantRules(input_dirname, musictype0)
	rules1 = getRelevantRules(input_dirname, musictype1)

	print(musictype0)
	rt = []
	for r in rules0[:10]:
		rt.append(','.join(map(str,r[:-1])) + '->' + str(r[-1]))

	print('\t'.join(rt))

	print(musictype1)
	rt = []
	for r in rules1[:10]:
		rt.append(','.join(map(str,r[:-1])) + '->' + str(r[-1]))
	print('\t'.join(rt))

	
	for i in [10,25,50,100]:
		r0, r1 = set(rules0[:i]), set(rules1[:i])
		s = np.round(len(r0.intersection(r1))/len(r0.union(r1)),2)
		l0 = np.round(np.mean([len(r) for r in r0]),2)
		l1 = np.round(np.mean([len(r) for r in r1]),2)

		c = r0.intersection(r1)
		t0 = [(',').join(map(str,r)) for r in rules0 if r in c]
		t1 = [(',').join(map(str,r)) for r in rules1 if r in c]
		rs, _ = np.round(stats.kendalltau(t0, t1),2)

		print('{}\t\t{}\t\t{}\t\t{}\t\t{}'.format(i, s, rs, l0, l1))


	r0, r1 = set(rules0), set(rules1)
	s = np.round(len(r0.intersection(r1))/len(r0.union(r1)),2)
	l0 = np.round(np.mean([len(r) for r in r0]),2)
	l1 = np.round(np.mean([len(r) for r in r1]),2)

	c = r0.intersection(r1)
	t0 = [(',').join(map(str,r)) for r in rules0 if r in c]
	t1 = [(',').join(map(str,r)) for r in rules1 if r in c]
	rs, _ = np.round(stats.kendalltau(t0, t1),2)

	print('{}\t\t{}\t\t{}\t\t{}\t\t{}'.format('All', s, rs, l0, l1))