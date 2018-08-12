import sys
import json
import csv
import os

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

def readData(fname):
	with open(fname, 'r') as f:
		jdata = json.load(f)

	trajectories = [] 				# all the trajectories

	for name in jdata:
		# Get pitch of song to convert to relative pitch
		pitch = jdata[name][0].split(' ')[0]
		pitch = pitch_map[pitch]

		mrow = [] 		# notes
		trow = []		# time intervals
		m_index = -1	# the index of mrow

		for i in jdata[name][1]:
			if len(jdata[name][1][i]) == 0:
				continue

			row = jdata[name][1][i]
			row = [int(r) if isinstance(r, int) else max(r) for r in row]			# In case of multiple notes at same position, select max
			#row = [r for r in row if r != 128] 									# Remove pause
			row = [r - pitch if r < 128 else r for r in row] 						# Convert to relative pitch (only non pauses)
			
			if len(row) > len(mrow):
				mrow = row
				m_index = i

		if m_index == -1:
			continue

		#t_max = jdata[name][2][m_index][-1][1]										# Length of the piece (used for normalization)
		trow = [(v[1]-v[0]) for v in jdata[name][2][m_index]]
		#print(trow)

		# Merge consecutive identical notes
		# Note: Optimize this 
		"""
		while True:
			dups = False
			for i in range(0, len(mrow)-2):
				if mrow[i] == mrow[i+1]:
					dups = True
					mrow.pop(i+1)
					trow[i] += trow[i+1]
					trow.pop(i+1)
					break
			if not dups:
				break
		"""

		# round the time
		trow = [round(v,1) for v in trow]

		# Filter out notes wih 0 interval
		"""
		traj = []
		for i in range(0, len(mrow)):
			traj.append('{}_{}'.format(mrow[i], trow[i]))
			
		trajectories.append(traj)
		"""
		trajectories.append(mrow)

		print('Processed: {}'.format(name))

	return trajectories


def saveTrajectory(data, sname):
	with open(sname, 'w') as f:
		writer = csv.writer(f, delimiter='\t')
		for row in data:
			writer.writerow(row)


if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]

	tdata = readData(fname)
	saveTrajectory(tdata, sname)
		