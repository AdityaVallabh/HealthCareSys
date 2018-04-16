
from healthcare.models import Hospital, Location
with open('./healthcare/data/hospitals.tsv') as f:
    lines = f.readlines()
    inserted = 0
    for rows in lines:
        row = rows.split('\t')
        if all(row):
            location, _ =  Location.objects.get_or_create(location_name=row[1])
            _, created = Hospital.objects.get_or_create(name = row[0], location = location, contact = row[2], email = row[3])
            print(created, inserted)
            if created:
                inserted += 1