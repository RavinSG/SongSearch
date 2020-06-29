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


def create_query(search_term, min_rating, artist_name, fuzzy=False, context=False):
    filters = []
    fuzziness = 0
    fields = ["track_name_si^3"]

    if context:
        fields.append("lyrics")

    if fuzzy:
        fuzziness = "AUTO"

    if min_rating is not None and min_rating != '' and float(min_rating) > 0:
        rating_facet = {
            "range": {
                "track_rating": {
                    "gte": float(min_rating)
                }
            }
        }

        filters.append(rating_facet)

    if artist_name != "":
        filters.append(search_artist(artist_name))

    query = {
        "bool": {
            "must": [{
                "multi_match": {

                    "query": search_term,
                    "fields": fields,
                    "fuzziness": fuzziness
                }
            }],
            "filter": filters
        }
    }

    return query


def search_top_songs():
    query = {
        "range": {
            "ranking": {
                "gte": 0
            }
        }
    }

    return query


def search_artist(artist_name):
    print("Artist filter added")
    artist_facet = {
        "match": {
            "artist_name_si": {
                "query": artist_name,
                "fuzziness": 0,
            }
        }
    }

    return artist_facet


def clean_search(search_term):
    stopwords = ["ගැන", "සින්දු"]
    words = search_term.split(" ")
    for word in words:
        if word in stopwords:
            words.remove(word)

    return " ".join(words)


def search(term: str, count: int, artist_name="", min_rating=0) -> List[SearchResult]:
    client = Elasticsearch()
    client.transport.connection_pool.connection.headers.update(HEADERS)
    context = False
    s = Search(using=client, index=INDEX_NAME, doc_type=DOC_TYPE)
    print(("t", term, artist_name, min_rating))

    if "*" in term:
        print("Wild card used")
        query = {
            "wildcard": {
                "track_name_si": term
            }
        }
        docs = s.query(query)[:count].execute()
        return [SearchResult.from_doc(d) for d in docs]

    if "ජනප්‍රියම" in term or "හොඳම" in term:
        print("Top result search executed")
        top_k = [int(s) for s in term.split() if s.isdigit()][0]
        query = search_top_songs()
        docs = s.query(query).sort("ranking")[:top_k].execute()

        return [SearchResult.from_doc(d) for d in docs]

    if "ගැන" in term or "පිළිබඳ" in term:
        context = True

    term = clean_search(term)
    query = create_query(term, min_rating, artist_name, context=context)
    docs = s.query(query)[:count].execute()

    if len(docs) < 3 and artist_name == '':
        query = create_query(term, min_rating, artist_name, fuzzy=True)
        docs = s.query(query)[:count].execute()
    #
    if len(docs) < 3 and artist_name != "" and term == "":
        print("Artist search executed")
        query = search_artist(artist_name)
        docs = s.query(query)[:count].execute()

    print("Final query: ", query)
    return [SearchResult.from_doc(d) for d in docs]
