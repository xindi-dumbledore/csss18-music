from mido import MidiFile
import sys

def readMidiFile(fname):
	mid = MidiFile(fname)
	for i, track in enumerate(mid.tracks):
		print('Track {}: {}'.format(i, track.name))
		for msg in track:
			print(msg)



if __name__ == '__main__':
	fname = sys.argv[1]
	readMidiFile(fname)