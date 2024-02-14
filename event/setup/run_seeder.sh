cd ..
python3 manage.py shell <<FOO
exec(open('setup/seed/seeder.py').read())
FOO
