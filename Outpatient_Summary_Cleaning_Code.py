""" Extracting data from CSV file """
import os
import csv

script_dir = os.path.dirname(__file__)
rel_path = 'outpatients.csv'
abs_file_path = os.path.join(script_dir, rel_path)
csv_file = open(abs_file_path, newline='')
csv_data = csv.DictReader(csv_file)


patients = []
visit = []
for rows in csv_data:
    patients.append(rows['Patient_ID'])
    visit.append(rows['Visit_ID'])


def get_columns(column):
    """Creates list of column's rows"""
    csv_file.seek(0)
    next(csv_data)
    empty = []
    for rows in csv_data:
        try:
            empty.append(rows[column])
        except NameError:
            empty.append('')
    return empty


def eliminate_nulls(combined_columns):
    """Eliminates blanks from lists"""
    clean = []
    for element in combined_columns:
        pt_clean = []
        for sublet in element:
            if sublet != '':
                pt_clean.append(sublet)
        clean.append(pt_clean)
    return clean


def patient_match(patients, column):
    """
    Matches column's rows to patients
    based on position (includes repeated values)
    """
    combo = {}
    for x, y in zip(patients, column):
        combo.setdefault(x, []).append(y)
    return combo


def combine_values(combo):
    """Combines all rows according to patient"""
    # Returns nested lists one list per row,
    # nested in a list per patient
    list_of_lists = []
    for values in combo.values():
        list_of_lists.append(values)
    return list_of_lists


def combine_ptrows(nested_lists):
    """Returns one list of values per patient"""
    submaster_columns = []
    for rows in nested_lists:
        sub = []
        for sublist in rows:
            for n in sublist:
                sub.append(n)
        submaster_columns.append(sub)
    return submaster_columns


def unique_items(column_list):
    """Returns number of unique values per patient"""
    unique_frequency = len(set(column_list))
    return unique_frequency


# Creates list of unique patients
pt_dict = patient_match(patients, visit)
unique_pt = []
for keys in pt_dict.keys():
    if keys not in unique_pt:
        unique_pt.append(keys)

# Finds number of visits per patient
visit_list = combine_values(pt_dict)

unique_visits = list(map(unique_items, visit_list))

patient_visits = dict(zip(unique_pt, unique_visits))


# Finds number of unique doctors per patient
doc_1 = get_columns('Primary_Physician')
doc_2 = get_columns('Operating_Physician')
doc_3 = get_columns('Other_Physician')
doc_total = list(zip(doc_1, doc_2, doc_3))

dr_seen = []
for item in doc_total:
    dr_seen.append(list(item))

clean_doclist = eliminate_nulls(dr_seen)
doc_dict = patient_match(patients, clean_doclist)
nested_docs = combine_values(doc_dict)
docs_list = combine_ptrows(nested_docs)
unique_docs = list(map(unique_items, docs_list))
patient_docs = dict(zip(unique_pt, unique_docs))

# Finds number of unique diagnoses per patient
icd_1 = get_columns('ICD9_DGNS_CD_1')
icd_2 = get_columns('ICD9_DGNS_CD_2')
icd_3 = get_columns('ICD9_DGNS_CD_3')
icd_4 = get_columns('ICD9_DGNS_CD_4')
icd_5 = get_columns('ICD9_DGNS_CD_5')
icd_6 = get_columns('ICD9_DGNS_CD_6')
icd_7 = get_columns('ICD9_DGNS_CD_7')
icd_8 = get_columns('ICD9_DGNS_CD_8')
icd_9 = get_columns('ICD9_DGNS_CD_9')
icd_10 = get_columns('ICD9_DGNS_CD_10')
icd_total = list(zip(icd_1, icd_2, icd_3, icd_4, icd_5,
                     icd_6, icd_7, icd_8, icd_9, icd_10))

list_icd_total = []
for item in icd_total:
    list_icd_total.append(list(item))

clean_icd = eliminate_nulls(list_icd_total)
icd_dict = patient_match(patients, clean_icd)

nested_icd = combine_values(icd_dict)

icd_list = combine_ptrows(nested_icd)

unique_icd = list(map(unique_items, icd_list))
patient_icd = dict(zip(unique_pt, unique_icd))

# Finds most common patient diagnosis
# Returns list of count per diagnosis per patient
pt_frequencies = []
for patient in icd_list:
    frequency = []
    for icd in patient:
        frequency.append(patient.count(icd))
    pt_frequencies.append(frequency)

# Returns nested lists of icds and counts
icd_count_list = []
for x, y in zip(icd_list, pt_frequencies):
    icd_count_list.append(list(zip(x, y)))

# Returns list with a dictionary per patient with counts
icd_pt_dict = []
for y in icd_count_list:
    icd_pt_dict.append(dict(y))

# Returns most common diagnosis per patient
common_icd = []
for icd in icd_pt_dict:
    for k, v in icd.items():
        common = []
        common.append(max(icd, key=icd.get))
    common_icd.append(common)

# Deletes nested list and matches values to patients
top_pt_icd = []
for enclosure in common_icd:
    for icd in enclosure:
        top_pt_icd.append(icd)
patient_common = dict(zip(unique_pt, top_pt_icd))

label_patient = ['Patient_ID']*26
label_visit = ['Total_Visits']*26
label_doctor = ['Total_Physicians']*26
label_diagnoses = ['Total_Diagnosis']*26
label_common = ['Most_Freq_Diganosis']*26

lp = list(zip(label_patient, unique_pt))
lv = list(zip(label_visit, unique_visits))
ldoc = list(zip(label_doctor, unique_docs))
licd = list(zip(label_diagnoses, unique_icd))
lc = list(zip(label_common, top_pt_icd))

master_list = list(zip(lp, lv, ldoc, licd, lc))
master_dictlist = []
for d in master_list:
    master_dictlist.append(dict(d))


with open('Outpatient_Summary.csv', 'w') as new_csv:
    fieldnames = ['Patient_ID', 'Total_Visits', 'Total_Physicians',
                  'Total_Diagnosis', 'Most_Freq_Diganosis']
    csv_writer = csv.DictWriter(new_csv, fieldnames=fieldnames,
                                lineterminator='\n')
    csv_writer.writeheader()
    csv_writer.writerows(master_dictlist)
