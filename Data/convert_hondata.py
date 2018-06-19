import sys
import json
import csv

def readData(fname):
	with open(fname, 'r') as f:
		jdata = json.load(f)
	
	data = []
	counter = 1
	for name in jdata:
		for i in jdata[name][1]:
			if len(jdata[name][1][i]) > 0:
				row = jdata[name][1][i]
				row = [r if isinstance(r, int) else max(r) for r in row]
				data.append(row)
				if counter == 724:
					print(name, i)
				counter += 1
	return data

def saveData(sname, data):
	with open(sname, 'w') as f:
		writer = csv.writer(f, delimiter=' ')
		for row in data:
			writer.writerow(row)


if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]

	data = readData(fname)
	#saveData(sname, data)
