# DirectoryOfRepositories

Setup
-------

To install, clone [this](https://github.com/mfraezz/DirectoryOfRepositories) repository and run:

```bash
pip install -Ur requirements.txt
```

To build the database, run:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py buildtables
```

Alternatively, if the database is broken or nonexistant, run:

```bash
sh clean_build.sh
```

This will delete the database if it exists, make a new one, and start the server.

If the database is not broken and you just want to start the server, run:

```bash
python manage.py runserver
```

and navigate to [http://localhost:8000/swag/](http://localhost:8000/swag/) to view a list of API endpoints.