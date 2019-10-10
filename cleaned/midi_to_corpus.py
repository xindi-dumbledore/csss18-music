"""This script reads in midi file and output the sequences for different tracks."""
from music21 import *
import json
from collections import defaultdict
import os
from glob import glob
import signal
import sys


class TimeoutException(Exception):
    """Custom exception class."""

    pass


def timeout_handler(signum, frame):
    """Custom signal handler."""
    raise TimeoutException

# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)


def quantify_music(piece):
    """
    The function to transform the piece into a dictionary encoding note sequence.

    Parameter:
    piece (music21 object): the music piece we want to extract sequence on

    Returns:
    (string): the key of the piece
    (dict): the midi sequence dictionary, key of dictionary denotes the track number
    (dict): the length of each note of midi sequence, key of dictionary denotes the track number.
    """
    # first pass of the music, not removing notes and rests that is not
    # reasonable
    midi_dict = {}
    time_dict = {}
    # tell us the key of the piece (eg. F major, C minor)
    key = piece.analyze('key').name
    duration_notes = []
    for i, p in enumerate(piece.parts):  # for different tracks
        part_midi = []
        time = []
        # secondsMap would include not only the note, but also the time
        # information
        for n in p.flat.notesAndRests.secondsMap:
            start = n['offsetSeconds']
            end = n['endTimeSeconds']
            time.append((start, end))
            element = n['element']
            try:
                part_midi.append(element.pitch.midi)
                if (end - start) != 0.0:
                    duration_notes.append((end - start))
            except:
                try:
                    part_midi.append([item.midi for item in element.pitches])
                except:
                    part_midi.append(128)  # coding rest as 128
        midi_dict[i] = part_midi
        time_dict[i] = time
    # Indentify short rest and long rest
    midi_dict_prune = defaultdict(list)
    time_dict_prune = defaultdict(list)
    min_threshold = min(duration_notes)
    max_threshold = max(duration_notes)
    for p in time_dict:
        for note, (start, end) in zip(midi_dict[p], time_dict[p]):
            if note != 128:
                midi_dict_prune[p].append(note)
                time_dict_prune[p].append((start, end))
            else:
                if end - start >= min_threshold:
                    if end - start > max_threshold:
                        midi_dict_prune[p].append(129)
                        time_dict_prune[p].append((start, end))
                    else:
                        midi_dict_prune[p].append(128)
                        time_dict_prune[p].append((start, end))
    return key, midi_dict_prune, time_dict_prune


def walk_dir(start_dir):
    """A helper function to get file name under a directory (including its subdirectory)."""
    midis = []
    pattern = "*.mid"
    for dir, _, _ in os.walk(start_dir):
        midis.extend(glob(os.path.join(dir, pattern)))
    return midis


def extract_corpus(midis, prefix="MIDI_Archive/", save_prefix="midi_corpus_", timeout=10):
    """
    The wrapper function to extract note sequences on a corpus.

    Parameter:
    midis (list): list of midi file directory
    prefix (string): indicate the location of the corpus
    save_prefix (string): saving name of the output
    timeout (int): the maximum process time allowed for each piece.
    """
    midi_corpus = {}
    count = 0
    ind = 0
    failed_midi = []
    big_midi = []
    for index, midi in enumerate(midis):
        if index % 100 == 0:
            print(index)
        # Start the timer. Once [timeout] seconds are over, a SIGALRM signal is
        # sent.
        signal.alarm(timeout)
        # This try/except loop ensures that TimeoutException is catched when
        # it's sent.
        try:
            try:
                piece = converter.parse(midi)
                key, midi_dict, duration_dict = quantify_music(piece)
                midi_corpus[midi.split(prefix)[1].split('.mid')[0].replace(
                    '/', ' ')] = [key, midi_dict, duration_dict]
                count += 1
            except:
                print("failed:", midi)
                failed_midi.append(midi)
        except TimeoutException:
            print("big:", midi)
            big_midi.append(midi)
            signal.alarm(0)
            continue  # continue the for loop if function A takes more than 5 second
        else:
            # Reset the alarm
            signal.alarm(0)
        if count > 200:
            json.dump(midi_corpus, open("%s_%s.json" %
                                        (save_prefix, ind), 'w'), indent=4)
            count = 0
            ind += 1
    json.dump(midi_corpus, open("%s_%s.json" %
                                (save_prefix, ind), 'w'), indent=4)


def main(argv):
    """The main function.

    Running example:
    python midi_to_sequence.py "MIDI_Archive/sample" "MIDI_Archive/" "midi_corpus"
    """
    directory, prefix, save_prefix = argv[1:]
    midis = walk_dir(directory)
    extract_corpus(midis, prefix, save_prefix)

if __name__ == '__main__':
    main(sys.argv)
