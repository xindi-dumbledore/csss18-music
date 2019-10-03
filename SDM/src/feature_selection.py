from sklearn.feature_selection import SelectKBest, chi2
import pandas as pd
import numpy as np
import sys






if __name__ == '__main__':
	fname = sys.argv[1]

	data = pd.read_csv(fname, sep='\t')
	#print(data)
	X = data.iloc[:,0:9]
	y = data.iloc[:,-2]

	f = SelectKBest(chi2, k='all').fit(X,y)

	print(X.columns)
	print(f.scores_)