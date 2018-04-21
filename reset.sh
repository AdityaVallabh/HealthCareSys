#!/usr/bin/env bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm db.sqlite3
python manage.py makemigrations accounts
python manage.py makemigrations healthcare
python manage.py makemigrations
python manage.py migrate
echo "exec(open('./healthcare/data/insert_hospitals.py').read());exec(open('./healthcare/data/insert_doctors.py').read())" | python manage.py shell
exit