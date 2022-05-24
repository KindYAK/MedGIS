import os
import pandas as pd

from gisapp.models import *

seen_names = set()
seen_regions = set()

def create_hospitals(df):
    hospitals = []
    for i, h in df.iterrows():
        if not h.hospital:
            continue
        hospital_name = str(h.hospital)[:500]
        if hospital_name in seen_names:
            continue
        if h.region not in seen_regions:
            r = Region.objects.create(name=h.region)
            d = District.objects.create(name="", region=r)
            Town.objects.create(name="", district=d)
            seen_regions.add(h.region)
        hospitals.append(
            Hospital(
                town=Town.objects.filter(district__region__name=h.region).first(),
                name=hospital_name,
                address=str(h.hospital_address)[:500],
            )
        )
        seen_names.add(hospital_name)
    Hospital.objects.bulk_create(hospitals, ignore_conflicts=True)


def create_cases(df):
    pass


def handle_file(file):
    print("Good", file)
    df = pd.read_csv(file)
    if len(df.columns) == 37:
        df.columns = ['ind', 'region',
           'hospital', 'illness_history',
           'rpnID', 'birth_date', 'death_date', 'age', 'sex',
           'citizenship', 'ethnicity', 'countryside', 'admission_date',
           'discharge_date', 'is_planned', 'is_urgent', 'from_where',
           'from_hospital', 'fix_hospital',
           'profile', 'stay_result', 'treatment_result', 'mkb_code',
           'diagnosis', 'diagnosis_type', 'is_diagnosis_final', 'surgery_code',
           'surgery_name', 'surgery_date', 'mkb_complication',
           'mkb_name', 'days_spent',
           'amount_to_pay', 'funding_source', 'hospital_address',
           'benefits', 'case_id']
    elif len(df.columns) == 42:
        print("!!! 42 columns file!")
        df.columns = ['ind', 'region',
                      'hospital', 'illness_history',
                      'rpnID', 'birth_date', 'death_date', 'age', 'sex',
                      'citizenship', 'ethnicity', 'countryside',
                      'blood', 'rezus', 'aids',
                      'admission_date', 'discharge_date', 'is_planned', 'is_urgent', 'from_where',
                      'from_hospital', 'fix_hospital',
                      'profile', 'stay_result', 'treatment_result', 'mkb_code',
                      'diagnosis', 'diagnosis_type', 'is_diagnosis_final', 'diagnosis_date',
                      'surgery_code', 'surgery_name', 'surgery_date', 'mkb_complication',
                      'mkb_name', 'days_spent',
                      'amount_to_pay', 'funding_source', 'hospital_address',
                      'benefits', 'social_status', 'case_id']
    else:
        raise Exception("Not implemented", len(df.columns))
    create_hospitals(df)
    create_cases(df)


root = "/is_ersb"
for cat in sorted(os.listdir(root)):
    print("!!!!", cat)
    for f in os.listdir(os.path.join(root, cat)):
        if f.endswith(".csv"):
            df = handle_file(os.path.join(root, cat, f))
        elif f.endswith(".xlsx"):
            continue
        else:
            print(f)
            for e in os.listdir(os.path.join(root, cat, f)):
                if e.endswith(".csv"):
                    df = handle_file(os.path.join(root, cat, f, e))
