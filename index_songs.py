from elasticsearch import Elasticsearch, helpers

from constants import DOC_TYPE, INDEX_NAME
from data import all_songs, SongData


def main():
    es = Elasticsearch()

    es.indices.delete(index=INDEX_NAME, ignore=404)
    es.indices.create(
        index=INDEX_NAME,
        body={
            'mappings': {
                DOC_TYPE: {
                    "properties": {
                        "situation": {
                            "type": "text"
                        },
                        "ranking": {
                            "type": "integer"
                        }
                    }
                }
            },
            'settings': {},
        },
    )

    bulk_index_songs(es, all_songs())


def bulk_index_songs(es, songs):
    actions = [
        {
            "_index": INDEX_NAME,
            "_type": DOC_TYPE,
            "_id": song.id,
            "_source": {
                "track_name_en": song.track_name_en,
                "track_name_si": song.track_name_si,
                "track_rating": float(song.track_rating),
                "album_name_en": song.album_name_en,
                "album_name_si": song.album_name_si,
                "artist_name_en": song.artist_name_en,
                "artist_name_si": song.artist_name_si,
                "artist_rating": song.artist_rating,
                "lyrics": song.lyrics,
                "ranking": float(song.ranking),
                "situation": song.situation
            }
        }
        for song in songs
    ]

    helpers.bulk(es, actions)

    print("Bulk indexed all songs")


if __name__ == '__main__':
    main()
