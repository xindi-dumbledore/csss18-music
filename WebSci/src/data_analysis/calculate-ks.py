import csv
from scipy import stats
import sys

def readData(fname, i):
	data = {}
	with open(fname, 'r') as f:
		reader = csv.reader(f, delimiter='\t')
		row = next(reader)
		print(row[i])
		for row in reader:
			label = row[-1]
			val = row[i]
			if label not in data:
				data[label] = []
			data[label].append(val)
	return data

def calculateKS(data):
	labels = list(data.keys())
	for i in range(0, len(labels)):
		for j in range(i+1, len(labels)):
			x = data[labels[i]]
			y = data[labels[j]]
			d,p = stats.ks_2samp(x,y)

			print('{} {}\t K: {} \t p: {}'.format(labels[i], labels[j], d, p))

if __name__ == '__main__':
	fname = sys.argv[1]
	ind = int(sys.argv[2])

	data = readData(fname, ind)
	calculateKS(data)