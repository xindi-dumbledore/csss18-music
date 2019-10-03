"""
Parallized function to generate features for a music corpus.
"""
import generate_features as features
import generate_gml as gml
import sys
import os
import csv
from multiprocessing import Pool
import signal


class TimeoutException(Exception):   # Custom exception class
    pass


def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

signal.signal(signal.SIGALRM, timeout_handler)


def getFiles(dirname, musictype):
    fnames = [f for f in os.listdir(
        dirname) if os.path.isfile(os.path.join(dirname, f))]
    fnames = [f for f in fnames if f.endswith('-network.csv')]
    fnames = [f for f in fnames if f.startswith(musictype)]
    return fnames


def saveData(sname, data, mlabel, song, t):
    with open(sname, 'a') as f:
        writer = csv.writer(f, delimiter='\t', quotechar='|')
        writer.writerow(data + [mlabel, song, t])


def parallelComputation(arg):
    """
    The parallel computation function to be parsed into pool.
    Parameter:
    arg (list): list of args, [graph_name, input_directory_name, genre_label]
    return:
    (list of features, process time for feature generation, graph name)
    """
    f = arg[0]
    input_dirname = arg[1]
    musiclabel = arg[2]
    print(f)
    try:
        edges = gml.getEdges(f, input_dirname)
        if len(edges) == 0:
            return
        graph = gml.generateGraph(edges)
        data, t = features.generateFeatures(graph, musiclabel)
        print(data, t)
        return data, t, f
    except:
        pass
    return None


if __name__ == '__main__':
    input_dirname = sys.argv[1]
    featurefile = sys.argv[2]
    labels = [('pop', 'POP'),
              ('metal', 'ROCK'),
              ('classical', 'CLASSICAL'),
              ('jazz', 'JAZZ'),
              ('american', 'FOLK')]

    for m in labels:
        musictype = m[0]
        musiclabel = m[1]
        fnames = getFiles(input_dirname, musictype)[:5]
        args = [[f, input_dirname, musiclabel] for f in fnames]
        with Pool(processes=1) as pool:
            results = pool.map(parallelComputation, args)
        for r in results:
            if r is None:
                continue
            saveData(featurefile, r[0], musiclabel, r[2], r[1])
