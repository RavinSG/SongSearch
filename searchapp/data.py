import json
import os
import textwrap

_all_songs = None


class SongData:

    def __init__(self, id_, track_id, track_name_en, track_name_si, track_rating, album_name_en,
                 album_name_si, artist_name_en, artist_name_si, artist_rating, lyrics, ranking):
        self.id = id_
        self.track_id = track_id
        self.track_name_en = track_name_en
        self.track_name_si = track_name_si
        self.track_rating = track_rating
        self.album_name_en = album_name_en
        self.album_name_si = album_name_si
        self.artist_name_en = artist_name_en
        self.artist_name_si = artist_name_si
        self.artist_rating = artist_rating
        self.lyrics = lyrics
        self.ranking = ranking

    def __str__(self):
        return textwrap.dedent("""\
            ID: {}
            Title (EN): {}
            Title (SI): {}
            Rating: {}
            Album (EN): {}
            Album (SI): {}
            Artist (EN): {}
            Artist (SI): {}
            Artist Rating: {}
            Lyrics (SI): {}
            Ranking: {}
        """).format(self.id,
                    self.track_name_en,
                    self.track_name_si,
                    self.track_rating,
                    self.album_name_en,
                    self.album_name_si,
                    self.artist_name_en,
                    self.artist_name_si,
                    self.artist_rating,
                    self.lyrics,
                    self.ranking)


dir_path = os.path.dirname(os.path.realpath(__file__))
file = open(os.path.join(dir_path, 'top_50.txt'))
count = 1
songs = []
for line in file:
    titles = line.split("<div class=\"title\">")
    for title in titles[1:]:
        count += 1
        songs.append(title.split("</div>")[0])


def all_songs():
    global _all_songs

    if _all_songs is None:
        _all_songs = []

        dir_path = os.path.dirname(os.path.realpath(__file__))
        songs_path = os.path.join(dir_path, 'songs.json')
        with open(songs_path, encoding='utf-8') as song_file:
            for idx, song in enumerate(json.load(song_file, strict=False)):
                id_ = idx + 1
                if song['track_name_en'] in songs:
                    song['ranking'] = songs.index(song['track_name_en'])
                else:
                    song['ranking'] = -1
                song_data = SongData(id_, **song)
                _all_songs.append(song_data)

    return _all_songs
