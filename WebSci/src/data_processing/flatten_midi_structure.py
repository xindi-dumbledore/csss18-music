import subprocess

if __name__ == '__main__':
	fname = 'midi.txt'
	target = '../csss18-music/Current/data/midi/'

	with open(fname, 'r') as f:
		line = f.readline().rstrip()
		while line:
			cmd = ['cp', line, target]
			subprocess.run(cmd)
			line = f.readline().rstrip()

