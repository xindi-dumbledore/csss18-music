import csv
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
#from imblearn.over_sampling import SMOTE
import sys
import numpy as np
from sklearn.model_selection import cross_validate
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score


def readFeatures(fname):
	data = {}
	with open(fname, 'r') as f:
		reader = csv.reader(f, delimiter='\t')
		next(reader)
		for row in reader:
			label = row[-1]
			features = list(map(float, row[:-1]))
			#features = list(map(float, row[:-4]))
			
			#features = [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
			features = list(map(float, features))
			
			#del features[5]								# Get rid of 5 because of high correlation
			features = [x if not np.isnan(x) else 0 for x in features]
			if label not in data:
				data[label] = []
			data[label].append(features)
	return data

def sampling(data, labels=None):
	"""
	Oversampling Using SMOTE
	"""
	X, y = [], []

	if labels is None:
		labels = set(data.keys())

	dcount = {l:len(data[l]) for l in labels}
	dsize = min(dcount.values())

	print(dsize)
	
	for l in labels:
		features = data[l]
		np.random.shuffle(features)
		features = features[:dsize]
		for d in features:
			X.append(d)
			y.append(l)

	#sm = SMOTE()
	#X, y = sm.fit_resample(X, y)

	return X, y


def classifyScores(clf, X,y):
	scoring = ['precision_macro', 'recall_macro', 'f1_macro', 'accuracy']
	scores = cross_validate(clf, X, y, cv=5, scoring=scoring)
	

	precision = [np.mean(scores['test_precision_macro']), np.std(scores['test_precision_macro'])]
	recall = [np.mean(scores['test_recall_macro']), np.std(scores['test_recall_macro'])]
	f1 = [np.mean(scores['test_f1_macro']), np.std(scores['test_f1_macro'])]
	accuracy = [np.mean(scores['test_accuracy']), np.std(scores['test_accuracy'])]

	return [precision[0], precision[1], recall[0], recall[1], f1[0], f1[1], accuracy[0], accuracy[1]]


def classifyScoresBinary(clf, X, y):
	scores = cross_validate(clf, X, y, cv=5, scoring=['roc_auc'])
	print(scores)

	return [np.mean(scores['test_roc_auc']), np.std(scores['test_roc_auc'])]


def saveClassificationResuts(sname, data):
	with open(sname, 'a+') as f:
		writer = csv.writer(f, delimiter='\t')
		for row in data:
			writer.writerow(row)


def featureImportance(X,y):
	clf = ExtraTreesClassifier(n_estimators=50)
	clf = clf.fit(X, y)
	print(clf.feature_importances_)


if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]

	#alg = 'SimpleNetwork'
	alg = 'MusicHON+'

	#labelslist = [['CLASSICAL','FOLK'], ['CLASSICAL','JAZZ'],['CLASSICAL','POP'],['CLASSICAL','ROCK'],['FOLK','JAZZ'],['FOLK','POP'],['FOLK','ROCK'],['JAZZ','ROCK'],['JAZZ','POP'],['POP','ROCK']]
	labelslist = [['MOZART','BACH'], ['MOZART','VIVALDI'],['MOZART','BEATLES'],['MOZART','NIRVANA'],['BACH','VIVALDI'],['BACH','BEATLES'],['BACH','NIRVANA'],['VIVALDI','BEATLES'],['VIVALDI','NIRVANA'],['BEATLES','NIRVANA']]

	#labelslist = [None, ['CLASSICAL','POP-ROCK'],['CLASSICAL','ROCK'],['POP','ROCK']]
	
	for labels in labelslist:
		if labels is None:
			classes = 'All'
		else:
			classes = '{}-{}'.format(labels[0],labels[1])

		results = []
		#labels = None

		data = readFeatures(fname)
		X, y = sampling(data, labels)

		featureImportance(X,y)
		clf_svm = svm.SVC(gamma='scale', decision_function_shape='ovo')
		#clf_svm = svm.LinearSVC()
		clf_rf = RandomForestClassifier(n_estimators=100)
		clf_mp = MLPClassifier(solver='lbfgs', activation='relu', alpha=1e-5, hidden_layer_sizes=(5, 5), learning_rate='adaptive')

		#results.append(classifyScores(clf_svm, X,y) + ['SVM', classes,'MusicHON'])
		#results.append(classifyScores(clf_rf, X, y) + ['RF', classes, 'MusicHON'])
		#results.append(classifyScores(clf_mp, X, y) + ['MLP', classes,'MusicHON'])

		results.append(classifyScoresBinary(clf_svm, X,y) + ['SVM', labels[0], labels[1], alg])
		results.append(classifyScoresBinary(clf_rf, X, y) + ['RF', labels[0], labels[1], alg])
		results.append(classifyScoresBinary(clf_mp, X, y) + ['MLP', labels[0], labels[1], alg])

		saveClassificationResuts(sname, results)
		for r in results:
			print(r)

