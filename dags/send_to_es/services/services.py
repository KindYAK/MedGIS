def send_db_to_es(**kwargs):
    from airflow.models import Variable

    from massmedia.models import Document
    from medgis.settings import ES_CLIENT, ES_INDEX_DOCUMENT

    from_id = Variable.get("db_to_es_from_id", default_var=0)
    try:
        to_id = Document.objects.latest('id').id
    except Document.DoesNotExist:
        to_id = None

    if not ES_CLIENT.indices.exists(ES_INDEX_DOCUMENT):
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

        mappings = {
            "properties": {
                "corpus": {
                    "type": "keyword"
                },
                "datetime": {
                    "type": "date"
                },
                "id": {
                    "type": "keyword"
                },
                "num_comments": {
                    "type": "integer"
                },
                "num_likes": {
                    "type": "integer"
                },
                "num_shares": {
                    "type": "integer"
                },
                "num_views": {
                    "type": "integer"
                },
                "source": {
                    "type": "keyword"
                },
                "text": {
                    "type": "text"
                },
                "title": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "url": {
                    "type": "keyword"
                },
            }
        }
        ES_CLIENT.indices.create(index=ES_INDEX_DOCUMENT, body={
            "settings": settings,
            "mappings": mappings
        }
    )

    send(from_id, to_id)

    Variable.set("db_to_es_from_id", to_id)
    return Variable.get("db_to_es_from_id", default_var=0)


def batch_qs(qs, batch_size=1000):
    total = qs.count()
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        yield qs[start:end]


def document_generator(qs):
    for batch in batch_qs(qs, batch_size=1000):
        for document in batch:
            yield {
                "id": document.id,
                "title": document.title,
                "text": document.text,
                "source": document.source.name,
                "corpus": document.source.corpus.name,
                "num_views": document.num_views,
                "num_comments": document.num_comments,
                "num_shares": document.num_shares,
                "num_likes": document.num_likes,
                "datetime": document.datetime,
                "url": document.url,
            }


def send(from_id, to_id):
    from elasticsearch.helpers import parallel_bulk

    from massmedia.models import Document
    from medgis.settings import ES_CLIENT, ES_INDEX_DOCUMENT

    qs = Document.objects.filter(id__gt=from_id)
    if to_id:
        qs = qs.filter(id__lte=to_id)
    qs = qs.order_by('id')

    print("Start build")
    success, failed = 0, 0
    number_of_documents = qs.count()
    for ok, result in parallel_bulk(ES_CLIENT, document_generator(qs), index=ES_INDEX_DOCUMENT,
                                    chunk_size=1000, raise_on_error=False, thread_count=4):
        if ok:
            success += 1
        else:
            failed += 1
            action, result = result.popitem()
            print("!!!", action, result)
        if failed > 3:
            raise Exception("Too many failed!!")
        if (success + failed) % 1000 == 0:
            print(f'{success + failed}/{number_of_documents} processed')
