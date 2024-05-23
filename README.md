# Python-Web-Application-Farrell-2023

Two of the most common production-ready high-performance WSGI servers are uWSGI and Gunicorn (short for Green Unicorn).

To run a Flask application using Gunicorn, you need to install it from the Python virtual environment with Flask:
``` commandline
(venv) ... $ pip install gunicorn
```

Run the webserver in a directory with `app.py`
``` commandline
$ gunicorn -w 4 app:app
```