Requirements
------------
* install with: pip install -r pip.txt


Setup
-----
1. Create settings.py from sample

        cp settings.py.sample settings.py

2. Create database (sqlite3), and admin account

        ./manage.py syncdb

3. Start local website on localhost:8000

        ./manage.py runserver


