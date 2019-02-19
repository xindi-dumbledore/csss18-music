import generate_features as features
import generate_gml as gml
import sys
import os
import csv
import networkx as nx

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


def saveData(sname, data, mlabel):
	with open(sname, 'a') as f:
		writer = csv.writer(f, delimiter='\t')
		writer.writerow(data.append(mlabel))

if __name__ == '__main__':
	input_dirname = sys.argv[1]
	#output_dirname = sys.argv[2]
	gml_dirname = sys.argv[2]
	featurefile = sys.argv[3]
	musictype = sys.argv[4]
	musiclabel = sys.argv[5]

	fnames = getFiles(input_dirname, musictype)

	for f in fnames:
		try:
			signal.alarm(60)

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
			saveData(featurefile, data, mlabel)
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
