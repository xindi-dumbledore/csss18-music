import sys
import json
import csv
import os

def readData(fname, sname):
	with open(fname, 'r') as f:
		jdata = json.load(f)
	
	#data = {}
	counter = 1
	for name in jdata:
		#data[name] = {}
		for i in jdata[name][1]:
			if len(jdata[name][1][i]) > 0:
				row = jdata[name][1][i]
				row = [r if isinstance(r, int) else max(r) for r in row]
				#data[name][i] = row
				if len(row) > 0:
					print('Saving : {} {}'.format(name, str(i)))
					print(os.path.join(sname, name[1:].replace('/', ' ') + '_' + i + '.csv'))
					saveData(os.path.join(sname, name[1:].replace('/', ' ') + '_' + i + '.csv'), row)
	
	#return data

def saveData(sname, data):
	with open(sname, 'w') as f:
		writer = csv.writer(f, delimiter=' ')
		writer.writerow(data)


if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]

	readData(fname, sname)
	#saveData(sname, data)
