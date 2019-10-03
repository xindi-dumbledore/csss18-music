from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
import pandas as pd 
import sys
import random
from sklearn.metrics.cluster import normalized_mutual_info_score
import seaborn as sns

def getData(fname):
	sample_size = 25

	df = pd.read_csv(fname, delimiter='\t')
	df = df.fillna(df.mean())

	df_classical = df[df['genre'] == 'CLASSICAL']
	df_jazz = df[df['genre'] == 'JAZZ']
	df_pop = df[df['genre'] == 'POP']
	df_rock = df[df['genre'] == 'ROCK']
	df_rockpop = pd.concat([df_pop, df_rock])
	df_rockpop['genre'] = 'POP_ROCK'
	df_folk = df[df['genre'] == 'FOLK']

	f = [1,2,4,6,8,]
	#f = range(0,11)

	cluster = AgglomerativeClustering(linkage='ward').fit(df_classical.iloc[:,f].values)
	index = [i for i in range(len(cluster.labels_)) if cluster.labels_[i] == 0]
	df_classical = df_classical.iloc[index,]

	cluster = AgglomerativeClustering(linkage='ward').fit(df_jazz.iloc[:,f].values)
	index = [i for i in range(len(cluster.labels_)) if cluster.labels_[i] == 0]
	df_jazz = df_jazz.iloc[index,]

	cluster = AgglomerativeClustering(linkage='ward').fit(df_rockpop.iloc[:,f].values)
	index = [i for i in range(len(cluster.labels_)) if cluster.labels_[i] == 0]
	df_rockpop = df_rockpop.iloc[index,]

	cluster = AgglomerativeClustering(linkage='ward').fit(df_folk.iloc[:,f].values)
	index = [i for i in range(len(cluster.labels_)) if cluster.labels_[i] == 0]
	df_folk = df_folk.iloc[index,]


	sample_classical = df_classical[:sample_size]
	#.sample(sample_size)
	sample_jazz = df_jazz[:sample_size]
	#.sample(sample_size)
	sample_rockpop = df_rockpop[:sample_size]
	#.sample(sample_size)
	sample_folk = df_folk[:sample_size]
	#.sample(sample_size)

	df = pd.concat([sample_folk, sample_rockpop, sample_jazz, sample_classical])

	features = df.iloc[:,f].values
	labels = df.iloc[:,-1].values
	
	return features, labels


def clustering(features, labels):
	#clustering = AgglomerativeClustering().fit(features)
	#print(set(labels))
	#print(labels)
	gcolors = {'POP_ROCK':'r', 'FOLK':'g', 'CLASSICAL':'b', 'JAZZ':'c'}
	colors = [gcolors[l] for l in labels]

	clustering = linkage(features, method='ward')

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



if __name__ == '__main__':
	fname = sys.argv[1]

	features, labels = getData(fname)
	cluster = AgglomerativeClustering(n_clusters=5, linkage='ward').fit(features)

	#print(cluster.labels_)
	#labels = cluster.labels_

	mi = normalized_mutual_info_score(cluster.labels_, labels)
	print(mi)
	
	gcolors = {'POP_ROCK':'r', 'FOLK':'g', 'CLASSICAL':'b', 'JAZZ':'c'}
	colors = [gcolors[l] for l in labels]
	g = sns.clustermap(features, method="ward", row_colors=colors, robust=True)
	plt.show()

	#clusters = clustering(features, labels)
	#print(clusters)

	#print(df.iloc[0,:].values)