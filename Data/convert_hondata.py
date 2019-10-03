import sys
import json
import csv
import os

#pitch_map = {'D minor', 'A- major', 'F minor', 'E- major', 'C major', 'E major', 'C# minor', 'C# major', 'F# minor', 'A major', 'B- major', 'A minor', 'G major', 'E- minor', 'B minor', 'F major', 'G minor', 'B- minor', 'D major', 'C minor', 'E minor'}

pitch_map = {
	'C':	60,
	'C#':	61,
	'D':	62,
	'D#':	63,
	'E':	64,
	'F': 	65,
	'F#':	66,
	'G':	67,
	'G#':	68,
	'A': 	69,
	'A#':	70,
	'B':	71,
	'D-':	61,
	'E-':	63,
	'F-':	64,
	'G-':	66,
	'A-':	68,
	'B-':	70 	
}

def readData(fname, sname):
	with open(fname, 'r') as f:
		jdata = json.load(f)
	
	#songs = ["Beatles Beatles_Yesterday", "Beatles Beatles_Blackbird", "Beatles Beatles_Eleanor_Rigby"]

	for name in jdata:
	#for name in songs:
		pitch = jdata[name][0].split(' ')[0]
		pitch = pitch_map[pitch]

		mrow = []

		for i in jdata[name][1]:
			if len(jdata[name][1][i]) > 0:
				row = jdata[name][1][i]
				row = [int(r) if isinstance(r, int) else max(r) for r in row]		# In case of multiple notes at same position, select max
				row = [r for r in row if r != 128] 								# Remove pause
				row = [r - pitch if r < 128 else r for r in row] 				# Convert to relative pitch
				#mrow = row
				#print(row)
				# Save only instrumet with most nodes
				if len(row) > len(mrow):
					mrow = thresholding(row)
					mrow = row
		if len(mrow) > 0:
			# Save the row with most notes
			try:
				print('Saving : {} {}'.format(name, str(i)))
			except:
				print('Saving')
			#print(os.path.join(sname, name.replace('/', ' ') + '_.csv'))
			saveData(os.path.join(sname, name.replace('/', ' ') + '_' + str(i) +' .csv'), mrow)
	
	#return data
	#print(set(pdata))


def thresholding(chords):
	"""
	Remove short rests, keep longer ones, and split into differet lines on very long rest
	"""
	#lower = 1
	#upper = 3

	chord_str = ' '.join(map(str, chords))
	chords = chord_str.split('129')
	chords = [c.split(' ') for c in chords]
	chords = [[int(i) for i in c if len(i) > 0] for c in chords]
	
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
