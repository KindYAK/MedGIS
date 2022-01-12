import datetime
import json

from elasticsearch_dsl import Search, Q
from rest_framework import viewsets
from rest_framework.response import Response

from medgis.settings import ES_CLIENT, ES_INDEX_DOCUMENT
from .serializers import *


class RangeDocumentsViewSet(viewsets.ViewSet):
    def search_search(self):
        date_from = datetime.datetime.strptime(self.request.GET['datetime_from'][:10], "%Y-%m-%d").date()
        date_to = datetime.datetime.strptime(self.request.GET['datetime_to'][:10], "%Y-%m-%d").date()
        s = Search(using=ES_CLIENT, index=ES_INDEX_DOCUMENT).source(('id', 'datetime', 'title', 'source', ))
        s = s.filter('range', datetime={"gte": date_from})
        s = s.filter('range', datetime={"lte": date_to})
        if self.request.GET['corpuses'] and self.request.GET['corpuses'] != "None":
            corpus_ids = json.loads(self.request.GET['corpuses'].replace("'", '"'))
            cs = Corpus.objects.filter(id__in=corpus_ids)
            s = s.filter('terms', **{"corpus": [c.name for c in cs]})
        if self.request.GET['sources'] and self.request.GET['sources'] != "None":
            sources_ids = json.loads(self.request.GET['sources'].replace("'", '"'))
            ss = Source.objects.filter(id__in=sources_ids)
            s = s.filter('terms', **{"source.keyword": [s.name for s in ss]})
        if self.request.GET['authors'] and self.request.GET['authors'] != "None":
            author_ids = json.loads(self.request.GET['authors'].replace("'", '"'))
            aus = Author.objects.filter(id__in=author_ids)
            s = s.filter('terms', **{"author.keyword": [a.name for a in aus]})
        if self.request.GET['title']:
            s = s.filter('match', title=self.request.GET['title'])
        if self.request.GET['text']:
            q = Q('multi_match',
                  query=self.request.GET['text'],
                  fields=['title^10',
                          'tags^3',
                          'categories^3',
                          'text^2'])
            s = s.query(q)
        s = s[:100]
        s.aggs.bucket(name="source", agg_type="terms", field="source.keyword") \
            .metric("source_weight", agg_type="sum", field="topic_weight")
        documents = s.execute()
        return documents, documents.aggregations.source.buckets

    def list(self, request):
        filter_type = request.GET['type']
        posneg_distribution = {}
        posneg_top_topics = {}
        posneg_bottom_topics = {}
        low_volume_positive_topics = {}
        if filter_type == "search":
            documents, source_buckets = self.search_search()
        else:
            return Response(
                {
                    "status": 400,
                    "error": "Search type not implemented",
                }
            )

        def get_value_or_weight(document):
            if hasattr(document, "weight") and document.weight:
                return round(document.weight, 3)
            if hasattr(document, "value") and document.value:
                return round(document.value, 3)
            if document.meta.score:
                return round(document.meta.score, 3) if document.meta.score != 0 else 1.000
            return 1

        if filter_type in ["topics", "search", "monitoring_object"]:
            source_weights = [
                        {
                            "source": bucket.key,
                            "weight": bucket.source_weight.value,
                        } for bucket in sorted(source_buckets, key=lambda x: x.source_weight.value, reverse=True)
                    ]
            documents = [
                {
                    "id": document.id,
                    "weight": get_value_or_weight(document),
                    "title": document.title,
                    "source": document.source,
                    "datetime": document.datetime,
                } for document in documents
            ]
        elif filter_type in ["criterions"]:
            posneg_distribution = dict(
                (key, [b.doc_count for b in bucket])
                for key, bucket in posneg_distribution.items()
            )
            posneg_top_topics = dict(
                (criterion_id, [bucket.to_dict() for bucket in buckets])
                    for criterion_id, buckets in posneg_top_topics.items()
            )
            posneg_bottom_topics = dict(
                (criterion_id, [bucket.to_dict() for bucket in buckets])
                    for criterion_id, buckets in posneg_bottom_topics.items()
            )
            source_weights = dict(
                ((criterion_id,
                    [
                        {
                            "source": bucket.key,
                            "weight": bucket.value,
                        } for bucket in sorted(buckets, key=lambda x: x.value, reverse=True)
                    ]
                ) if buckets and hasattr(buckets[0], "doc_count") else (criterion_id, buckets)) for criterion_id, buckets in source_buckets.items()
            )
            for document in documents:
                document["document"] = {
                    "id": document["document"].id,
                    "title": document["document"].title,
                    "source": document["document"].source,
                    "datetime": document["document"].datetime,
                }
        else:
            return Response(
                {
                    "status": 400,
                    "error": "Search type not implemented",
                }
            )

        return Response(
            {
                "status": 200,
                "documents": documents,
                "source_weights": source_weights,
                "posneg_distribution": posneg_distribution,
                "posneg_top_topics": posneg_top_topics,
                "posneg_bottom_topics": posneg_bottom_topics,
                "low_volume_positive_topics": low_volume_positive_topics
            }
        )
