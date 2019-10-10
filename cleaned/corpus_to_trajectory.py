import sys
import json
import csv
import os

pitch_map = {
    'C': 60,
    'C#': 61,
    'D': 62,
    'D#': 63,
    'E': 64,
    'F': 65,
    'F#': 66,
    'G': 67,
    'G#': 68,
    'A': 69,
    'A#': 70,
    'B': 71,
    'D-': 61,
    'E-': 63,
    'F-': 64,
    'G-': 66,
    'A-': 68,
    'B-': 70
}


def readData(fname, genre):
    """
    Convert the corpus file into a csv file recording note sequence of each piece of a given genre

    Parameters:
    fname(string): directory to midi corpus
    genre(string): indicate the genre we want to extract

    Return:
    (list): the trajectory list
    """
    with open(fname, 'r') as f:
        jdata = json.load(f)
    trajectories = []  # all the trajectories
    for name in jdata:
        if not name.startswith(genre):
            continue
        # Get pitch of song to convert to relative pitch
        pitch = jdata[name][0].split(' ')[0]
        pitch = pitch_map[pitch]
        mrow = []         # record the trajectory with the most number of notes
        for i in jdata[name][1]:
            if len(jdata[name][1][i]) == 0:
                continue
            row = jdata[name][1][i]
            # In case of multiple notes at same position, select max
            row = [int(r) if isinstance(r, int) else max(r) for r in row]
            # Convert to relative pitch (only non pauses)
            row = [r - pitch if r < 128 else r for r in row]
            if len(row) > len(mrow):
                mrow = row
        trajectories.append(mrow)
    return trajectories


def saveTrajectory(data, sname):
    """
    Save the trajectory to a csv file.

    Parameters:
    data(list): the trajectory we want to save
    sname(string): save file name
    """
    with open(sname, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    """
    Running example: python corpus_to_trajectory.py midi_corpus_0.json sample_trajectory.csv sample
    """
    fname, sname, genre = sys.argv[1:]
    tdata = readData(fname, genre)
    saveTrajectory(tdata, sname)
