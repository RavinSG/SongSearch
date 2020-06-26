import json
import os
import textwrap

_all_songs = None


class SongData:

    def __init__(self, id_, track_id, track_name_en, track_name_si, track_rating, album_name_en,
                 album_name_si, artist_name_en, artist_name_si, artist_rating, lyrics):
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
        """).format(self.id,
                    self.track_name_en,
                    self.track_name_si,
                    self.track_rating,
                    self.album_name_en,
                    self.album_name_si,
                    self.artist_name_en,
                    self.artist_name_si,
                    self.artist_rating,
                    self.lyrics)


def all_songs():
    """
    Returns a list of ~2,200 SongData objects, loaded from
    searchapp/songs.json
    """

    global _all_songs

    if _all_songs is None:
        _all_songs = []

        # Load the songs json from the same directory as this file.
        dir_path = os.path.dirname(os.path.realpath(__file__))
        songs_path = os.path.join(dir_path, 'songs.json')
        with open(songs_path,encoding='utf-8') as song_file:
            for idx, song in enumerate(json.load(song_file, strict=False)):
                id_ = idx + 1  # ES indexes must be positive integers, so add 1
                song_data = SongData(id_, **song)
                _all_songs.append(song_data)

    return _all_songs
