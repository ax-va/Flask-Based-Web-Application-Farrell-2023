# Python-Web-Application-Farrell-2023

Two of the most common production-ready high-performance WSGI servers are uWSGI and Gunicorn (short for Green Unicorn).

To run a Flask application using Gunicorn, you need to install it in the Python virtual environment with Flask:
```unix
(venv) ... $ pip install gunicorn
```

Run the webserver in a directory with `app.py` with four worker instances:
```unix
$ gunicorn -w 4 app:app
```
The first part,`app`, corresponds to `app.py`. The second part, `:app`, refers to the Flask application instance created in `app.py`:
```python
app = Flask(__name__)
```

The recommended number of workers for an application running on a single production server is 
`number_of_CPU_cores * 2 + 1`.
