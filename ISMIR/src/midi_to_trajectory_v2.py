"""
this version will output three trajectory:
1) the longest part
2) the second longest one
3) the one with the lowest
"""
import sys
import json
import numpy as np

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


def readData(fname):
    jdata = json.load(open(fname))
    print(len(jdata))
    longest_data = {} 				# all the trajectories
    second_longest_data = {}
    lowest_data = {}
    genre_map = {'metal_rock': 'ROCK',
                 'pop': 'POP',
                 'classical': 'CLASSICAL',
                 'jazz': 'JAZZ',
                 'american_folk': 'FOLK'}
    for name in jdata:
        piece_genre = ""
        for genre in genre_map:
            if name.lower().startswith(genre):
                piece_genre = genre
                break
        if piece_genre == "":
            print(name)
            continue
        # Get pitch of song to convert to relative pitch
        pitch = jdata[name][0].split(' ')[0]
        pitch = pitch_map[pitch]
        longest_row = [] 		# notes
        second_longest_row = []
        lowest_row = []
        temp_rows = []
        temp_pitch_rows = []
        for i in jdata[name][1]:
            if len(jdata[name][1][i]) == 0:
                continue
            row = jdata[name][1][i]
            # In case of multiple notes at same position, select max
            row = [int(r) if isinstance(r, int) else max(r) for r in row]
            pitch_row = [r for r in row if r < 128]
            temp_pitch_rows.append(pitch_row)
            # row = [r for r in row if r != 128] 									# Remove pause
            # Convert to relative pitch (only non pauses)
            row = [r - pitch if r < 128 else r for r in row]
            temp_rows.append(row)
        row_len = list(map(len, temp_rows))
        row_pitch = [np.mean([r for r in row if r < 128]) for row in temp_pitch_rows]
        longest_i = np.argsort(row_len)[-1]
        try:
            second_longest_i = np.argsort(row_len)[-2]
        except:
            second_longest_i = np.argsort(row_len)[-1]
        lowest_i = np.argsort(row_pitch)[-1]
        second_longest_row = temp_rows[second_longest_i]
        longest_row = temp_rows[longest_i]
        lowest_row = temp_rows[lowest_i]
        longest_data[name] = {'trajectory': longest_row,
                              'pitch': pitch, 'genre': genre_map[piece_genre]}
        second_longest_data[name] = {'trajectory': second_longest_row,
                                     'pitch': pitch, 'genre': genre_map[piece_genre]}
        lowest_data[name] = {'trajectory': lowest_row,
                             'pitch': pitch, 'genre': genre_map[piece_genre]}
        try:
            print('Processed: {}'.format(name))
        except:
            pass
    return longest_data, second_longest_data, lowest_data


def saveTrajectory(longest_data, second_longest_data, lowest_data, sname):
    lines = []
    f = open(sname, "w")
    for name in longest_data:
        info = list(map(str, [longest_data[name]["genre"], name,
                              "longest"] + longest_data[name]["trajectory"]))
        lines.append('\t'.join(info) + '\n')
    for name in second_longest_data:
        info = list(map(str, [second_longest_data[name][
                    "genre"], name, "second_longest"] + second_longest_data[name]["trajectory"]))
        lines.append('\t'.join(info) + '\n')
    for name in lowest_data:
        info = list(map(str, [lowest_data[name]["genre"], name,
                              "lowest"] + lowest_data[name]["trajectory"]))
        lines.append('\t'.join(info) + '\n')
    f.writelines(lines)
    f.close()


if __name__ == '__main__':
    fname = sys.argv[1]
    sname = sys.argv[2]
    longest_data, second_longest_data, lowest_data = readData(fname)
    saveTrajectory(longest_data, second_longest_data, lowest_data, sname)

# python midi_to_trajectory_v2.py midi_corpus_larger.json trajectory_corpus_v2.csv
