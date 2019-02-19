import csv
import sys

def readData(fname, label):
	data = []
	with open(fname, 'r') as f:
		reader = csv.reader(f, delimiter='\t')
		next(reader)
		for row in reader:
			data.append(row + [label])

	return data

def saveData(sname, data):
	with open(sname, 'a+') as f:
		writer = csv.writer(f, delimiter='\t')
		for row in data:
			writer.writerow(row)

if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]
	label = sys.argv[3]

	data = readData(fname, label)
	saveData(sname, data)
