import csv
import sys
import numpy as np

def readData(fname, artist, data=None):
	if data is None:
		data = [[] for _ in range(0,16)]
	with open(fname, 'r') as f:
		reader = csv.reader(f, delimiter='\t')
		next(reader)
		for row in reader:
			if artist not in str(row[-2]):
				continue
			for i in range(0, len(row)-3):
				data[i].append(float(row[i]))
			data[-1].append(artist.upper())

	return data

def saveData(sname, data):
	ndata = [[] for _ in range(0, len(data[0]))]
	#print(len(ndata), len(data[0]))
	for row in data:
		row = list(row)
		for i in range(0, len(row)):
			#print(i, len(ndata[i]), len(row))
			ndata[i].append(row[i])

	with open(sname, 'a+') as f:
		writer = csv.writer(f, delimiter='\t')
		for row in ndata:
			writer.writerow(row)


def normalize(data):
	"""
	ndata = []
	for i in range(0, 12):
		row = []
		for r in data:
			row.append(r[i])
		ndata.append(row)

	print(ndata)
	"""
	ndata = []
	for i in range(0, len(data)-1):
		row = [x if not np.isnan(x) else 0 for x in data[i]]

		m = np.mean(row)
		s = np.std(row)

		if np.isnan(m):
			for x in data[i]:
				if np.isnan(x):
					print(x)
		
		print(m,s)
		ndata.append([(x - m)/s for x in data[i]])
	
	ndata.append(data[-1])
	return ndata


if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]

	artists = ['mozart', 'bach', 'vivaldi', 'beatles', 'nirvana']
	data = None
	for a in artists:
		data = readData(fname, a, data)

	data = normalize(data)
	saveData(sname, data)
