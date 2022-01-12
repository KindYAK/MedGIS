import datetime
import json
import math
import os
import pytz

import pandas as pd
from annoying.functions import get_object_or_None
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from massmedia.models import *
from medgis.settings import MEDIA_ROOT


class Command(BaseCommand):
    @staticmethod
    def row_str_parser(row, param_name):
        return row[param_name] if (param_name in row) and (type(row[param_name]) == str) else None

    @staticmethod
    def row_int_parser(row, param_name):
        return int(row[param_name]) if (param_name in row) and (row[param_name]) and (not math.isnan(row[param_name])) else None

    def handle(self, *args, **options):
        max_len = Document._meta.get_field('title').max_length
        corpus = get_object_or_None(Corpus, name="main")
        if not corpus:
            corpus = Corpus.objects.create(name="main")
        chunksize = 50000
        db_chunksize = 10000
        for filename in os.listdir(os.path.join(MEDIA_ROOT, "output_fr")):
            print("NEW FILE", filename)
            dfs = pd.read_csv(os.path.join(MEDIA_ROOT, "output_fr", filename), chunksize=chunksize)
            documents = []
            source_dict = {}
            for i, df in enumerate(dfs, start=1):
                for index, row in df.iterrows():
                    media_name = row['source']
                    if media_name in source_dict:
                        source = source_dict[media_name]
                    else:
                        source = get_object_or_None(Source, name=media_name, corpus=corpus)
                        if not source:
                            source = Source.objects.create(name=media_name, url=media_name, corpus=corpus)
                        source_dict[media_name] = source

                    date = None
                    if row.get('datetime', None) and type(row['datetime']) == str:
                        try:
                            date = datetime.datetime.strptime(row['datetime'][:-6], "%Y-%m-%d")
                        except:
                            try:
                                date = datetime.datetime.strptime(row['datetime'][:-6], "%Y-%m-%dT%H:%M:%S")
                            except:
                                date = datetime.datetime.strptime(row['datetime'][:-6], "%Y-%m-%dT%H:%M:%S.%f")
                        date = date.replace(tzinfo=pytz.timezone('Asia/Almaty'))

                    if not row['title'] or type(row['title']) != str:
                        continue

                    if not row['text'] or type(row['text']) != str:
                        continue

                    if Document.objects.filter(source=source, datetime=date, title=row['title']).exists():
                        continue

                    document = Document(
                        source=source,
                        datetime=date,
                        text=self.row_str_parser(row, 'text'),
                        title=self.row_str_parser(row, 'title')[:max_len] if self.row_str_parser(row, 'title') else None,
                        url=self.row_str_parser(row, 'url'),
                        num_views=self.row_int_parser(row, 'num_views'),
                    )

                    documents.append(document)
                    if len(documents) % db_chunksize == 0:
                        Document.objects.bulk_create(documents, ignore_conflicts=True)
                        documents = []
                print(i * chunksize)
            Document.objects.bulk_create(documents, ignore_conflicts=True)
