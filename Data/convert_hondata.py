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
				rows = thresholding(row)
				if len(rows) > 0:
					print('Saving : {} {}'.format(name, str(i)))
					print(os.path.join(sname, name[1:].replace('/', ' ') + '_' + i + '.csv'))
					saveData(os.path.join(sname, name[1:].replace('/', ' ') + '_' + i + '.csv'), rows)
	
	#return data


def thresholding(chords):
	"""
	Remove short rests, keep longer ones, and split into differet lines on very long rest
	"""
	#lower = 1
	#upper = 3

	chord_str = ' '.join(map(str, chords))
	chords = chord_str.split('128 128 128')
	chords = [c.replace('128 128', '128') for c in chords]
	chords = [c.replace('128', '') for c in chords]
	chords = [c.split(' ') for c in chords]
	chords = [[int(i) for i in c if len(i) > 0] for c in chords]
	#chord_str = chord_str.replace('128', '')
	return chords


def saveData(sname, data):
	with open(sname, 'w') as f:
		writer = csv.writer(f, delimiter=' ')
		for row in data:
			writer.writerow(row)


if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]

	readData(fname, sname)
	#saveData(sname, data)
