import os
import pandas as pd

from gisapp.models import *

def handle_file(file):
    print("Good", file)
    df = pd.read_csv(file)
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
    return df

root = "/is_ersb"
for cat in os.listdir(root):
    print("!!!!", cat)
    for f in os.listdir(os.path.join(root, cat)):
        if f.endswith(".csv"):
            df = handle_file(os.path.join(root, cat, f))
            break
        elif f.endswith(".xlsx"):
            continue
        else:
            print(f)
            for e in os.listdir(os.path.join(root, cat, f)):
                if e.endswith(".csv"):
                    df = handle_file(os.path.join(root, cat, f, e))
                    break
