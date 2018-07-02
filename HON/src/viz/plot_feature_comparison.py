import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import sys
import os


def readFeature(fname):
    data = {'weighted_abruptness': [], 'branchiness_mean': [],
            'unweighted_abruptness': [], 'melodic_mean': [],
            'repeteadness_mean': [], 'melodic_variance': [],
            'repeteadness_variance': [], 'pitch_in_rules': [],
            'pitch_in_piece': [], 'branchiness_variance': [],
            'pitch_between_rules': []}

    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        for row in reader:
            #row = list(map(float, row))
            data['melodic_variance'].append(float(row[0]))
            data['repeteadness_mean'].append(float(row[1]))
            data['repeteadness_variance'].append(float(row[2]))
            data['pitch_in_piece'].append(float(row[3]))
            data['weighted_abruptness'].append(float(row[4]))
            data['pitch_in_rules'].append(float(row[5]))
            data['branchiness_mean'].append(float(row[6]))
            # print(row[7][1:-1].split(','))
            if len(row[7][1:-1].split(',')) > 1:
                data['pitch_between_rules'].append(
                    np.mean([float(r) for r in row[7][1:-1].split(',')]))
            else:
                data['pitch_between_rules'].append(0)
            data['branchiness_variance'].append(float(row[8]))
            data['melodic_mean'].append(float(row[9]))
            data['unweighted_abruptness'].append(float(row[10]))
    return data


def plotDistribution(data, dtype, xname, sname, log=False):
    plt.clf()
    plt.figure(figsize=(20, 20))
    names = list(data.keys())
    pdata = [[v for v in data[n][dtype] if not np.isnan(
        v) and not np.isinf(v)] for n in names]

    # print(pdata)

    fig, ax = plt.subplots()
    for i in range(0, len(pdata)):
        m = np.mean(pdata[i])
        sns.distplot(pdata[i], kde_kws={"lw": 1, "label": names[
                     i]}, hist=False, rug=False, kde=True, ax=ax, color=sns.color_palette()[i])
        plt.vlines(m, ymin=0, ymax=3, lw=1.5,
                   color=sns.color_palette()[i], linestyles="--")
    ax.set(xlabel=xname, ylabel='KDE')
    if log:
        plt.xscale('log')
    # plt.show()

    plt.savefig(sname, dpi=1000, bbox_inches='tight')
    # plt.clf()


if __name__ == '__main__':
    dirname = sys.argv[1]
    # sname = sys.argv[2]

    data = {}
    data['American Folk'] = readFeature(
        os.path.join(dirname, 'folk_larger_aggregate.csv'))
    data['Rock'] = readFeature(os.path.join(
        dirname, 'rock_larger_aggregate.csv'))
    data['Classical'] = readFeature(os.path.join(
        dirname, 'classical_larger_aggregate.csv'))
    data['Jazz'] = readFeature(os.path.join(
        dirname, 'jazz_larger_aggregate.csv'))
    data['Pop'] = readFeature(os.path.join(
        dirname, 'pop_larger_aggregate.csv'))

    #names = ['American Folk', 'Rock', 'Classical', 'Jazz', 'Pop']

    #branchiness = [folk['branchiness_mean'], rock['branchiness_mean'], classic['branchiness_mean'], jazz['branchiness_mean'], pop['branchiness']]
    #uabruptness = [folk['unweighted_abruptness'], rock['unweighted_abruptness'], classic['unweighted_abruptness'], jazz['unweighted_abruptness'], pop['unweighted_abruptness']]
    #wabruptness = [folk['weighted_abruptness'], rock['weighted_abruptness'], classic['weighted_abruptness'], jazz['weighted_abruptness'], pop['weighted_abruptness']]

    plotDistribution(data, 'branchiness_mean', 'Branchiness (Mean)',
                     "../../feature_comparison/branchiness.pdf", False)
    plotDistribution(data, 'weighted_abruptness', 'Weighted Abruptness',
                     "../../feature_comparison/weighted_abruptness.pdf", True)
    plotDistribution(data, 'unweighted_abruptness', 'Unweighted Abruptness',
                     "../../feature_comparison/unweighted_abruptness.pdf", True)
    plotDistribution(data, 'melodic_mean', 'Melodic (Mean)',
                     "../../feature_comparison/melodic_mean.pdf", False)
    #plotDistribution(uabruptness, names, 'Unweighted Abruptness', True)
    #plotDistribution(wabruptness, names, 'Weighted Abruptness', True)
