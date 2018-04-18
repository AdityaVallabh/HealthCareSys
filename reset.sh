find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py makemigrations accounts
python3 manage.py makemigrations healthcare
python3 manage.py migrate
echo "exec(open('./healthcare/data/insert_hospitals.py').read());exec(open('./healthcare/data/insert_doctors.py').read())" | python3 manage.py shell
exit