Requirements
============
* python-openid - if you want to use OpenID authentication


Setup
=====
1. Create settings.py from sample

	cp settings.py.sample settings.py

2. Create database (sqlite3), and admin account

	./manage.py syncdb

3. Load sample data

	./scripts/loaddata.sh

4. Start local website on localhost:8000

	./manage.py runserver


