import pandas as pd

from gisapp.models import MKBClass

df = pd.read_excel("/mkb.xlsx")
df = df.sort_values('level')

for i in [4, 3, 2, 1, 0]:
    MKBClass.objects.filter(level=i).delete()

cur_level = None
batch = []
for i, (_, c) in enumerate(df.iterrows()):
    if i % 100 == 0:
        print(f"{i}/{len(df)}")
    if (cur_level != c['level'] and batch) or len(batch) == 1000:
        print("! BATCH", cur_level, len(batch))
        MKBClass.objects.bulk_create(batch)
        batch = []
    if cur_level != c['level']:
        cur_level = c['level']
    batch.append(
        MKBClass(
            name=c['name'],
            code=c['code'],
            level=c['level'],
            parent=MKBClass.objects.get(code=c['parent']) if c['parent'] != "No" else None
        )
    )

if batch:
    MKBClass.objects.bulk_create(batch)
    batch = []
