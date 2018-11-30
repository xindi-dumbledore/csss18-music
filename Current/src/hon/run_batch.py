import sys
import os
import main

if __name__ == '__main__':
	InputDirName = sys.argv[1]
	OutputDirName = sys.argv[2]

	fnames = [f for f in os.listdir(InputDirName) if os.path.isfile(os.path.join(InputDirName, f))]

	for f in fnames:
		InputFileName = os.path.join(InputDirName, f)
		OutputNetworkFile = os.path.join(OutputDirName, '{}-{}'.format(f[:-4], 'network.csv'))
		OutputRulesFile = os.path.join(OutputDirName, '{}-{}'.format(f[:-4], 'rules.csv'))

		main.BuildHON(InputFileName, OutputNetworkFile, OutputRulesFile)