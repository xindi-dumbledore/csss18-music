import sys
import csv
import os

if __name__ == '__main__':
	InputDirName = sys.argv[1]

	fnames = [os.path.join(InputDirName, f) for f in os.listdir(InputDirName) if os.path.isfile(os.path.join(InputDirName, f))]
	i = 1
	
	for fn in fnames:
		print('{} of {} File: {}'.format(i, len(fnames), fn))
		try:
			data = []
			with open(fn, 'r') as f:
				reader = csv.reader(f, delimiter=' ')
				for row in reader:
					data.append(['T'] + row)
				f.close()

			with open(fn, 'w') as f:
				writer = csv.writer(f, delimiter=' ')
				for row in data:
					writer.writerow(row)
		except:
			pass
