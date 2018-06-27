import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import sys
import os

def readFeature(fname):
	data = {'weighted_abruptness':[], 'branchiness_mean':[],\
	 'unweighted_abruptness':[], 'melodic_mean':[],\
	 'repeteadness_mean':[], 'melodic_variance':[],\
	 'repeteadness_variance':[], 'pitch_in_rules':[],\
	 'pitch_in_piece':[], 'branchiness_variance':[]}

	with open(fname, 'r') as f:
		reader = csv.reader(f, delimiter='\t')
		next(reader)
		for row in reader:
			row = list(map(float, row))
			data['melodic_variance'].append(row[0])
			data['repeteadness_mean'].append(row[1])
			data['repeteadness_variance'].append(row[2])
			data['pitch_in_piece'].append(row[3])
			data['weighted_abruptness'].append(row[4])
			data['pitch_in_rules'].append(row[5])
			data['branchiness_mean'].append(row[6])
			data['branchiness_variance'].append(row[7])
			data['melodic_mean'].append(row[8])
			data['unweighted_abruptness'].append(row[9])
	return data

def plotDistribution(data, dtype, xname, log=False):
	names = list(data.keys())
	pdata = [data[n][dtype] for n in names]

	fig, ax = plt.subplots()
	for i in range(0, len(pdata)):
		m = np.mean(pdata[i])
		sns.distplot(pdata[i], kde_kws={"lw": 1, "label": names[i]}, hist=False, rug=False, kde=True, ax=ax, color = sns.color_palette()[i])
		plt.vlines(m, ymin=0, ymax=m, lw=1, color = sns.color_palette()[i])
	ax.set(xlabel=xname, ylabel='KDE')
	if log:
		plt.xscale('log')
	plt.show()


if __name__ == '__main__':
	dirname = sys.argv[1]

	data = {}
	data['American Folk'] = readFeature(os.path.join(dirname, 'american_folk_aggregate.csv'))
	data['Rock'] = readFeature(os.path.join(dirname, 'rock_aggregate.csv'))
	data['Classical'] = readFeature(os.path.join(dirname, 'classical_aggregate.csv'))
	data['Jazz'] = readFeature(os.path.join(dirname, 'jazz_aggregate.csv'))
	data['Pop'] = readFeature(os.path.join(dirname, 'pop_aggregate.csv'))


	#names = ['American Folk', 'Rock', 'Classical', 'Jazz', 'Pop']
	
	#branchiness = [folk['branchiness_mean'], rock['branchiness_mean'], classic['branchiness_mean'], jazz['branchiness_mean'], pop['branchiness']]
	#uabruptness = [folk['unweighted_abruptness'], rock['unweighted_abruptness'], classic['unweighted_abruptness'], jazz['unweighted_abruptness'], pop['unweighted_abruptness']]
	#wabruptness = [folk['weighted_abruptness'], rock['weighted_abruptness'], classic['weighted_abruptness'], jazz['weighted_abruptness'], pop['weighted_abruptness']]


	plotDistribution(data, 'melodic_mean', 'Melodic (Mean)', False)
	#plotDistribution(uabruptness, names, 'Unweighted Abruptness', True)
	#plotDistribution(wabruptness, names, 'Weighted Abruptness', True)