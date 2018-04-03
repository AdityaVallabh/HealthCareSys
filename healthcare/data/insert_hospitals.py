
from healthcare.models import Hospital
with open('./healthcare/data/hospitals.tsv') as f:
    lines = f.readlines()
    for rows in lines:
        row = rows.split('\t')
        if all(row):
            _, created = Hospital.objects.get_or_create(name = row[0], location = row[1], contact = row[2], email = row[3])
