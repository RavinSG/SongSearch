from elasticsearch import Elasticsearch, helpers

from searchapp.constants import DOC_TYPE, INDEX_NAME
from searchapp.data import all_products, ProductData


def main():
    # Connect to localhost:9200 by default.
    es = Elasticsearch()

    es.indices.delete(index=INDEX_NAME, ignore=404)
    es.indices.create(
        index=INDEX_NAME,
        body={
            'mappings': {
                DOC_TYPE: {  # This mapping applies to products.
                    'properties': {  # Just a magic word.
                        'name': {  # The field we want to configure.
                            'type': 'text',  # The kind of data we’re working with.
                            'fields': {  # create an analyzed field.
                                'english_analyzed': {  # Name that field `name.english_analyzed`.
                                    'type': 'text',  # It’s also text.
                                    'analyzer': 'custom_english_analyzer',  # And here’s the analyzer we want to use.
                                }
                            }
                        },
                        'description': {  # The field we want to configure.
                            'type': 'text',  # The kind of data we’re working with.
                            'fields': {  # create an analyzed field.
                                'english_analyzed': {  # Name that field `name.english_analyzed`.
                                    'type': 'text',  # It’s also text.
                                    'analyzer': 'custom_english_analyzer',  # And here’s the analyzer we want to use.
                                }
                            }
                        }
                    }
                }
            },
            'settings': {
                'analysis': {  # magic word.
                    'analyzer': {  # yet another magic word.
                        'custom_english_analyzer': {  # The name of our analyzer.
                            'type': 'english',  # The built in analyzer we’re building on.
                            'stopwords': ['made', '_english_'],  # Our custom stop words, plus the defaults.
                        },
                    },
                },
            },
        },
    )

    # index_product(es, all_products())
    products_to_index(es, all_products())


def products_to_index(es, products: [ProductData]):
    actions = [
        {
            "_index": INDEX_NAME,
            "_type": DOC_TYPE,
            "_id": j,
            "_source": {
                "name": product.name,
                "image": product.image,
                "price": product.price,
                "description": product.description
            }

        }
        for j, product in enumerate(products)
    ]

    helpers.bulk(es, actions)
    print("Indexed all products")


def index_product(es, products: [ProductData]):
    """Add a single product to the ProductData index."""
    prod_id = 1
    for product in products:
        es.create(
            index=INDEX_NAME,
            doc_type=DOC_TYPE,
            id=prod_id,
            body={
                "name": product.name,
                "image": "http://placekitten.com/200/200",
            }
        )

        prod_id += 1

    # Don't delete this! You'll need it to see if your indexing job is working,
    # or if it has stalled.
    # print("Indexed {}".format(product.name))
    print("Indexed all products")


if __name__ == '__main__':
    main()
