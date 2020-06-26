from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from typing import List

from searchapp.constants import DOC_TYPE, INDEX_NAME

HEADERS = {'content-type': 'application/json'}


class SearchResult:
    """Represents a product returned from elasticsearch."""

    def __init__(self, id_, track_name_si, track_name_en):
        self.id = id_
        self.track_name_si = track_name_si
        self.track_name_en = track_name_en

    def from_doc(doc) -> 'SearchResult':
        print(doc)
        return SearchResult(
            id_=doc.meta.id,
            track_name_en=doc.track_name_en,
            track_name_si=doc.track_name_si,
        )


def search(term: str, count: int, artist_name=None, min_rating=0) -> List[SearchResult]:
    client = Elasticsearch()
    # Elasticsearch 6 requires the content-type header to be set, and this is
    # not included by default in the current version of elasticsearch-py
    client.transport.connection_pool.connection.headers.update(HEADERS)

    s = Search(using=client, index=INDEX_NAME, doc_type=DOC_TYPE)
    filters = []

    if min_rating != '' and float(min_rating) > 0:
        rating_facet = {
            "range": {
                "track_rating": {
                    "gte": float(min_rating)
                }
            }
        }

        filters.append(rating_facet)

    if artist_name is not None and artist_name != '':
        artist_facet = {
            "match": {
                "artist_name_si": {
                    "query": artist_name,
                    "fuzziness": "AUTO"
                }
            }
        }

        filters.append(artist_facet)

    query = {
        "bool": {
            "must": [{
                "match": {
                    "track_name_si": {
                        "query": term,
                        "fuzziness": "AUTO"
                    }
                }
            }],
            "filter": filters
        }
    }

    print(query)
    docs = s.query(query)[:count].execute()

    return [SearchResult.from_doc(d) for d in docs]
