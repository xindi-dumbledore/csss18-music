import requests
import json
import sqlite3
import tables
import os
import csv

MUSICBRAINZ_TRACK_URL = ["https://musicbrainz.org/ws/2/recording/?query=recording:","%20AND%20artist:","%20AND%20resease:","&fmt=json"]


# Files
LMD_SCORES = 'dataset/unprocessed/lmd_match_scores.json'
LMD_META = 'dataset/unprocessed/lmd_matched_h5'
DB_FILE = 'dataset/genre.csv'

# Utility functions for retrieving paths
def msd_id_to_dirs(msd_id):
	"""Given an MSD ID, generate the path prefix.
	E.g. TRABCD12345678 -> A/B/C/TRABCD12345678"""
	return os.path.join(msd_id[2], msd_id[3], msd_id[4], msd_id)

def msd_id_to_mp3(msd_id):
	"""Given an MSD ID, return the path to the corresponding mp3"""
	return os.path.join(DATA_PATH, 'msd', 'mp3',
						msd_id_to_dirs(msd_id) + '.mp3')

def msd_id_to_h5(h5):
	"""Given an MSD ID, return the path to the corresponding h5"""
	return os.path.join(LMD_META,
						msd_id_to_dirs(msd_id) + '.h5')


def get_scores():
	with open(LMD_SCORES) as f:
		scores = json.load(f)
	return scores

def get_recording_info(msd_id):
	recording, artist, release, genre = None, None, None, []

	with tables.open_file(msd_id_to_h5(msd_id)) as h5:
		recording = h5.root.metadata.songs.cols.title[0]
		artist = h5.root.metadata.songs.cols.artist_name[0]
		release = h5.root.metadata.songs.cols.release[0]

		name = list(h5.root.musicbrainz.artist_mbtags)
		count = list(h5.root.musicbrainz.artist_mbtags_count)

		genre = [[name[i], count[i]] for i in range(len(name))]
		print('{} by {} on {}'.format(recording, artist, release))

	return recording, artist, release, genre


def getTrackGenre(recording, artist, release):
	url = "{}{}{}{}{}{}{}".format(MUSICBRAINZ_TRACK_URL[0], recording, MUSICBRAINZ_TRACK_URL[1], artist, MUSICBRAINZ_TRACK_URL[2], release, MUSICBRAINZ_TRACK_URL[3])
	response = requests.get(url)
	jdata = json.loads(response.text)['recordings']
	
	tags = []

	for j in jdata:
		if "tags" in j:
			tags += [[t['name'], t['count']] for t in j['tags']]

	dtags = {}
	for t in tags:
		name = t[0]
		count = t[1]
		if name not in dtags:
			dtags[name] = 0
		dtags[name] += count

	tags = [[name, dtags[name]] for name in dtags]

	return tags


def insertToDB(fnames, recording, artist, release, agenre, rgenre):
	data = []
	for f in fnames:
		data += [(f, recording, artist, release, str(genre[0]), genre[1], "artist") for genre in agenre]
		data += [(f, recording, artist, release, str(genre[0]), genre[1], "recording") for genre in rgenre]

	with open(DB_FILE, 'a+') as f:
		writer = csv.writer(f, delimiter='\t', quotechar="'", quoting=csv.QUOTE_MINIMAL)

		for row in data:
			writer.writerow(row)

	
	#print(data)
	#cur = conn.cursor()
	#cur.executemany("""INSERT INTO genre (fname, recording, artist, release, genre_name, genre_count, genre_type) VALUES (?, ?, ?, ?, ?, ?, ?)""", data)
	#conn.commit()


if __name__ == '__main__':

	scores = get_scores()

	for msd_id in scores:
		try:
			recording, artist, release, agenre = get_recording_info(msd_id)
			rgenre = getTrackGenre(recording, artist, release)
			fnames = scores[msd_id].keys()

			insertToDB(fnames, recording, artist, release, agenre, rgenre)
		except:
			print('Error!!')
			pass


