from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from typing import List

from searchapp.constants import DOC_TYPE, INDEX_NAME

HEADERS = {'content-type': 'application/json'}


class SearchResult:
    """Represents a product returned from elasticsearch."""

    def __init__(self, id_, track_name_si, artist_name_si):
        self.id = id_
        self.track_name_si = track_name_si
        self.artist_name_si = artist_name_si

    def from_doc(doc) -> 'SearchResult':
        print(doc)
        return SearchResult(
            id_=doc.meta.id,
            artist_name_si=doc.artist_name_si,
            track_name_si=doc.track_name_si,
        )


def create_query(search_term, min_rating, artist_name, fuzzy=False):
    filters = []
    fuzziness = 0
    if fuzzy:
        fuzziness = "AUTO"

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
                    "fuzziness": fuzziness
                }
            }
        }

    query = {
        "bool": {
            "must": [{
                "multi_match": {

                    "query": search_term,
                    "fields": ["track_name_si^2", "lyrics"],
                    "fuzziness": fuzziness
                }
            }],
            "filter": filters
        }
    }

    return query


def search(term: str, count: int, artist_name=None, min_rating=0) -> List[SearchResult]:
    client = Elasticsearch()
    # Elasticsearch 6 requires the content-type header to be set, and this is
    # not included by default in the current version of elasticsearch-py
    client.transport.connection_pool.connection.headers.update(HEADERS)

    s = Search(using=client, index=INDEX_NAME, doc_type=DOC_TYPE)

    query = create_query(term, min_rating, artist_name)

    print(query)
    docs = s.query(query)[:count].execute()
    if len(docs) < 3:
        query = create_query(term, min_rating, artist_name, fuzzy=True)
        docs = s.query(query)[:count].execute()

    return [SearchResult.from_doc(d) for d in docs]
