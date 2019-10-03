import sys
import os
import main
import BuildRulesFastParameterFree
import BuildRulesFastParameterFreeFreq
import BuildNetwork
import itertools
from collections import defaultdict

MaxOrder = 99
MinSupport = 1

def buildHON(InputFileName, OutputRulesFile, OutputNetworkFile):
	RawTrajectories = main.ReadSequentialData(InputFileName)
	TrainingTrajectory, TestingTrajectory = main.BuildTrainingAndTesting(RawTrajectories)
	main.VPrint(len(TrainingTrajectory))
	#Rules = BuildRulesFastParameterFreeFreq.ExtractRules(TrainingTrajectory, MaxOrder, MinSupport)
	Rules = BuildRulesFastParameterFree.ExtractRules(TrainingTrajectory, MaxOrder, MinSupport)
	main.DumpRules(Rules, OutputRulesFile)
	BuildNetwork.Initialize()
	Network = BuildNetwork.BuildNetwork(Rules)
	main.DumpNetwork(Network, OutputNetworkFile)


if __name__ == '__main__':
	InputDirName = sys.argv[1]
	OutputDirName = sys.argv[2]

	fnames = [f for f in os.listdir(InputDirName) if os.path.isfile(os.path.join(InputDirName, f))]
	i = 0
	for f in fnames:
		InputFileName = os.path.join(InputDirName, f)
		OutputNetworkFile = os.path.join(OutputDirName, '{}-{}'.format(f[:-4], 'network.csv'))
		OutputRulesFile = os.path.join(OutputDirName, '{}-{}'.format(f[:-4], 'rules.csv'))

		#main.BuildHON(InputFileName, OutputNetworkFile, OutputRulesFile)

		print('Processing: {}'.format(f))

		#try:
		#buildHON(InputFileName, OutputRulesFile, OutputNetworkFile)
		main.BuildHON(InputFileName, OutputNetworkFile, OutputRulesFile)
		#except:
		#	pass

		i += 1
		if i > 10:
			break