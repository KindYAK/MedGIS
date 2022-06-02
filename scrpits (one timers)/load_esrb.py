import datetime
import os

import pandas as pd

from gisapp.models import *

seen_names = set()
seen_regions = set()

def create_hospitals(df):
    hospitals = []
    for _, h in df.iterrows():
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

Citizenship.objects.all().delete()
Ethnicity.objects.all().delete()
StayProfile.objects.all().delete()
SurgeryType.objects.all().delete()
FundingSource.objects.all().delete()

citizenships_dict = dict()
ethnicity_dict = dict()
profile_dict = dict()
surgery_dict = dict()
funding_source_dict = dict()
def create_cases(df):
    cases = []
    for _, c in df.iterrows():
        # print("!!!")
        # print(c)
        hospital_name = str(c.hospital)[:500]
        citizenship = str(c.citizenship).strip()
        ethnicity = str(c.ethnicity).strip()
        profile = str(c.profile).strip()
        surgery_code = str(c.surgery_code).strip()
        surgery_name = str(c.surgery_name).strip()
        funding_source = str(c.funding_source).strip()
        mkb_code = str(c.mkb_code).strip()
        if mkb_code not in mkb_dcit:
            mkb_dcit[mkb_code] = MKBClass.objects.create(code=mkb_code, name=c.diagnosis, level=99)
        if citizenship not in citizenships_dict:
            citizenships_dict[citizenship] = Citizenship.objects.create(name=citizenship)
        if ethnicity not in ethnicity_dict:
            ethnicity_dict[ethnicity] = Ethnicity.objects.create(name=ethnicity)
        if profile not in profile_dict:
            profile_dict[profile] = StayProfile.objects.create(name=profile)
        if surgery_code not in surgery_dict:
            surgery_dict[surgery_code] = SurgeryType.objects.create(name=surgery_name, code=surgery_code)
        if funding_source not in funding_source_dict:
            funding_source_dict[funding_source] = FundingSource.objects.create(name=funding_source)
        cases.append(
            PatientStay(
                hospital=hospitals_dict[hospital_name] if hospital_name in hospitals_dict else None,
                from_hospital=hospitals_dict[str(c.from_hospital)[:500]] if str(c.from_hospital)[:500] in hospitals_dict else None,
                fix_hospital=hospitals_dict[str(c.fix_hospital)[:500]] if str(c.fix_hospital)[:500] in hospitals_dict else None,
                citizenship=citizenships_dict[citizenship],
                ethnicity=ethnicity_dict[ethnicity],
                surgery=surgery_dict[surgery_code],
                funding_source=funding_source_dict[funding_source] if funding_source in funding_source_dict else None,
                profile=profile_dict[profile],
                mkb_complication=mkb_dcit[str(c.mkb_complication).strip()] if str(c.mkb_complication).strip() in mkb_dcit else None,
                mkb=mkb_dcit[mkb_code] if mkb_code in mkb_dcit else None,
                birth_date=datetime.datetime.strptime(str(c.birth_date).strip(), "%d.%m.%Y").strftime("%Y-%m-%d") if str(c.birth_date).strip().lower() not in ['', None, 'nan', 'none', 'null'] else None,
                death_date=datetime.datetime.strptime(str(c.death_date).strip(), "%d.%m.%Y").strftime("%Y-%m-%d") if str(c.death_date).strip().lower() not in ['', None, 'nan', 'none', 'null'] else None,
                admission_date=datetime.datetime.strptime(str(c.admission_date).strip(), "%d.%m.%Y").strftime("%Y-%m-%d") if str(c.admission_date).strip().lower() not in ['', None, 'nan', 'none', 'null'] else None,
                discharge_date=datetime.datetime.strptime(str(c.discharge_date).strip(), "%d.%m.%Y").strftime("%Y-%m-%d") if str(c.discharge_date).strip().lower() not in ['', None, 'nan', 'none', 'null'] else None,
                surgery_date=datetime.datetime.strptime(str(c.surgery_date).strip(), "%d.%m.%Y").strftime("%Y-%m-%d") if str(c.surgery_date).strip().lower() not in ['', None, 'nan', 'none', 'null'] else None,
                sex=0 if str(c.sex).lower().strip() == "мужской" else 1,
                is_diagnosis_final=str(c.is_diagnosis_final).strip() == "Заключительный",
                countryside=0 if str(c.countryside).lower().strip() == "село" else 1,
                is_planned=bool(int(c.is_planned)),
                is_urgent=bool(int(c.is_urgent)),
                from_where=c.from_where,
                stay_result=dict([('Выписан', 0), ('Переведен', 1), ('Самовольный уход', 2), ('Умер', 3)]).get(str(c.stay_result).strip(), 0),
                treatment_result=dict([('Выздоровление', 0), ('Смерть', 1), ('Без перемен', 2), ('Ухудшение', 3), ('Улучшение', 4), ('Переведен в круглосуточный стационар', 5)]).get(str(c.treatment_result).strip(), 0),
                diagnosis_type=dict([('Основное', 0), ('Сопутствующее', 1), ('Уточняющее', 2), ('Осложнение', 3)]).get(str(c.diagnosis_type).strip(), 0),
                illness_history=c.illness_history,
                rpnID=c.rpnID,
                age=c.age,
                diagnosis=c.diagnosis,
                days_spent=max(min(c.days_spent, 1000), 0),
                benefits=c.benefits,
                case_id=c.case_id,
                amount_to_pay=c.amount_to_pay,
           )
        )
    PatientStay.objects.bulk_create(cases, ignore_conflicts=True)


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


PatientStay.objects.all().delete()
hospitals_dict = dict(
    (h.name, h) for h in Hospital.objects.all()
)
mkb_dcit = dict(
    (c.code, c) for c in MKBClass.objects.all()
)
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
