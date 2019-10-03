import generate_features as features
import generate_gml as gml
import sys
import os
import csv
import networkx as nx
from multiprocessing import Pool
import numpy as np

# ----- Part to set timeout if something takes too 
import signal

class TimeoutException(Exception):   # Custom exception class
	pass

def timeout_handler(signum, frame):   # Custom signal handler
	raise TimeoutException

# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)
# ---- Part to set timeout if something takes too long


def getFiles(dirname, musictype):
	fnames = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
	fnames = [f for f in fnames if f.endswith('-network.csv')]
	fnames = [f for f in fnames if f.startswith(musictype)]
	return fnames


def saveData(sname, data, mlabel, song, t):
	with open(sname, 'a') as f:
		writer = csv.writer(f, delimiter='\t', quotechar='|')
		writer.writerow(data + [mlabel, song, t])


def parallelComputation(arg):
	f = arg[0]
	input_dirname = arg[1]
	musiclabel = arg[2]
	print(f)
	try:
		edges = gml.getEdges(f, input_dirname)
		if len(edges) == 0:
			return
		graph = gml.generateGraph(edges)
		
		#print(nx.info(graph))

		data, t = features.generateFeatures(graph, musiclabel)
		print(data, t)
		#saveData(featurefile, data, musiclabel, f, t)

		return data, t, f
	except:
		pass
	return None


if __name__ == '__main__':
	input_dirname = sys.argv[1]
	featurefile = sys.argv[2]
	#musictype = sys.argv[3]
	#musiclabel = sys.argv[4]

	labels = [('pop','POP'),('metal','ROCK'),('classical','CLASSICAL'),('jazz','JAZZ'),('american','FOLK')]

	for m in labels:
		musictype = m[0]
		musiclabel = m[1]

		fnames = getFiles(input_dirname, musictype)[:5]
		#np.random.shuffle(fnames)
		#fnames = fnames[:500]

		args = [[f,input_dirname,musiclabel] for f in fnames]

		with Pool(processes=1) as pool:
			results = pool.map(parallelComputation, args)

		for r in results:
			if r is None:
				continue
			saveData(featurefile, r[0], musiclabel, r[2], r[1])


	"""
	for f in fnames:
		if i > 50:
			break
		try:
			print('Processing: \t {}'.format(f))
			

			i += 1

			#break
		except:
			pass

		#break
	"""
	"""
		try:
			signal.alarm(1800)

			# If a particular file takes too long , skip it
			print('Processing: \t {}'.format(f))
			edges = gml.getEdges(f, input_dirname)
			if len(edges) == 0:
				continue
			graph = gml.generateGraph(edges)
			#drawGraph(graph, output_dirname, f)
			#gml.saveGML(graph, gml_dirname, 'network.gml')

			print(nx.info(graph))

			print('Generated Graph.')

			data = features.generateFeatures(graph)
			print(data)
			#saveData(featurefile, data, musiclabel, f)
		except:
		#	print('Error')
		#	pass
			# handle the exception
			signal.alarm(0)
			print('Timeout')
			continue # continue the for loop if function A takes more than 10 second
		else:
			# Reset the alarm
			signal.alarm(0)

	#features.saveData(featurefile, data, mlabel)
	"""
