from random import randrange
from healthcare.models import Hospital, Department
from accounts.models import DoctorProfile
from django.contrib.auth.models import User
from django.db import transaction
inserted = 0
with open('./healthcare/data/doctors.tsv') as f:
    lines = f.readlines()
    with transaction.atomic():
        for rows in lines:
            row = rows.split('\t')
            full_name = row[1].split(' ')
            first_name, last_name = full_name[0], full_name[-1]
            username = first_name + last_name + str(inserted)
            contact = row[2]
            specialization = row[3].replace('\n','')
            email = username + '@gmail.com'
            password = 'pass123'
            hospital = Hospital.objects.get(pk=(randrange(15)+1))
            specialization, _ = Department.objects.get_or_create(department_name=specialization)
            user, created = User.objects.get_or_create(username=username, first_name=first_name, last_name=last_name, email=email)
            print(created, inserted)
            if created:
                user.set_password(password)
                user.save()
                _, created = DoctorProfile.objects.get_or_create(user=user, hospital=hospital, contact=contact, specialization=specialization)
                inserted += 1
