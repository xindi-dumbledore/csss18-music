from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
import pandas as pd 
import sys
import random
from sklearn.metrics.cluster import normalized_mutual_info_score
import seaborn as sns
from sklearn.cluster import SpectralClustering
from scipy.spatial import distance
import numpy as np
import csv
from sklearn.decomposition import PCA


def getData(fname):
	#sample_size = 200

	df = pd.read_csv(fname, delimiter='\t')
	df = df.fillna(df.mean())

	#f = range(0,13)
	f = range(0,6)

	df_classical = df[df['genre'] == 'CLASSICAL']
	df_jazz = df[df['genre'] == 'JAZZ']
	df_pop = df[df['genre'] == 'POP']
	df_rock = df[df['genre'] == 'ROCK']
	df_folk = df[df['genre'] == 'FOLK']

	df = pd.concat([df_classical, df_jazz, df_pop, df_rock, df_rock, df_folk])

	"""
	sample_classical = df_classical.sample(sample_size)
	sample_jazz = df_jazz.sample(sample_size)
	sample_pop = df_pop.sample(sample_size)
	sample_rock = df_rock.sample(sample_size)
	sample_folk = df_folk.sample(sample_size)

	df = pd.concat([sample_folk, sample_rock, sample_pop, sample_jazz, sample_classical])
	#df = pd.concat([sample_folk, sample_classical])
	"""
	

	features = df.iloc[:,f].values
	labels = df.iloc[:,-1].values
	
	return features, labels


def getDataArtist(fname):
	df = pd.read_csv(fname, delimiter='\t')
	df = df.fillna(df.mean())

	#f = range(0,13)
	f = range(0,6)

	df_0 = df[df['genre'] == 'MOZART']
	df_1 = df[df['genre'] == 'BACH']
	df_2 = df[df['genre'] == 'VIVALDI']
	df_3 = df[df['genre'] == 'BEATLES']
	df_4 = df[df['genre'] == 'NIRVANA']

	df = pd.concat([df_0, df_1, df_2, df_3, df_4])

	features = df.iloc[:,f].values
	labels = df.iloc[:,-1].values
	
	return features, labels


def principleComponents(features, labels):
	pca = PCA(n_components=3)
	x = pca.fit_transform(features)

	print('PCA Variance', pca.explained_variance_ratio_)

	return [np.append(x[i], [labels[i]]) for i in range(len(x))]



def agglomerativeClustering(features, labels):
	#clustering = AgglomerativeClustering().fit(features)
	#print(set(labels))
	#print(labels)
	gcolors = {'POP':'r', 'FOLK':'g', 'CLASSICAL':'b', 'JAZZ':'c', 'ROCK':'m'}
	colors = [gcolors[l] for l in labels]

	clustering = linkage(features, method='ward', optimal_ordering=True)

	link_cols = {}
	for i, i12 in enumerate(clustering[:,:2].astype(int)):
		c1, c2 = (link_cols[x] if x > len(clustering) else colors[x] for x in i12)
		link_cols[i+1+len(clustering)] = c1 if c1 == c2 else "#808080"

	#print(link_cols)
	#print(len(colors), len(features))
	
	plt.figure(figsize=(15, 7))
	dendrogram(clustering,
			orientation='top',
            labels=labels,
            no_labels=False,
            distance_sort='descending',
            link_color_func=lambda k: link_cols[k])
	plt.show()
	#print('Number of clusters: {}'.format(clustering.n_clusters))
	#return clustering.labels_


def spectralClustering(features, lables):
	clustering = SpectralClustering(n_clusters=5, assign_labels="discretize").fit(features)
	print(clustering.labels_)

	mi = normalized_mutual_info_score(clustering.labels_, labels)
	print(mi)


def clusterMap(features, labels):
	gcolors = {'POP':'r', 'FOLK':'g', 'CLASSICAL':'b', 'JAZZ':'c', 'ROCK':'m'}
	colors = [gcolors[l] for l in labels]
	g = sns.clustermap(features, method="ward", row_colors=colors, robust=True)
	plt.show()


def saveData(sname, data):
	with open(sname, 'w+') as f:
		writer = csv.writer(f, delimiter='\t')
		for r in data:
			writer.writerow(r)


def distanceMatrix(features, labels):
	dmat, rdist = {}, []
	for i in range(len(features)):
		l0 = labels[i]
		f0 = features[i]
		if l0 not in dmat:
			dmat[l0] = {}
		for j in range(len(features)):
			l1 = labels[j]
			f1 = features[j]
			if l1 not in dmat[l0]:
				dmat[l0][l1] = []
			d = distance.euclidean(f0, f1)
			dmat[l0][l1].append(d)
			rdist.append((i,j,d,l0,l1))

	for l0 in dmat:
		for l1 in dmat[l0]:
			dmat[l0][l1] = (np.mean(dmat[l0][l1]), np.std(dmat[l0][l1]))
			print('{}\t{}\t{}\t{}'.format(l0,l1, dmat[l0][l1][0], dmat[l0][l1][1]))

	
	return rdist



if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]

	#features, labels = getData(fname)
	features, labels = getDataArtist(fname)

	pc = principleComponents(features, labels)
	saveData(sname, pc)

	#rdist = distanceMatrix(features, labels)
	#saveData(sname, rdist)

	#spectralClustering(features, labels)
	#agglomerativeClustering(features, labels)
	#clusterMap(features, labels)

	"""
	cluster = AgglomerativeClustering(n_clusters=5, linkage='ward').fit(features)

	#print(cluster.labels_)
	#labels = cluster.labels_

	mi = normalized_mutual_info_score(cluster.labels_, labels)
	print(mi)
	
	
	"""

	#clusters = clustering(features, labels)
	#print(clusters)

	#print(df.iloc[0,:].values)