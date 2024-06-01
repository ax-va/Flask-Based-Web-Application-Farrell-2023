# Python-Web-Application-Farrell-2023

## WSGI

Two of the most common production-ready high-performance WSGI servers are uWSGI and Gunicorn (short for Green Unicorn).

To run a Flask application using Gunicorn, you need to install it in the Python virtual environment with Flask:
```unix
(venv) ... $ pip install gunicorn
```

Run the webserver with four worker instances in a directory with `app.py`
```unix
$ gunicorn -w 4 app:app
```
or in a directory with `blog.py`
```
$ gunicorn -w 4 blog:app
```
The first part,`app` or `blog`, corresponds to `app.py` or `blog.py`, respectively. The second part, `:app`, refers to the Flask application instance created in `app.py` or `blog.py`:
```python
app: Flask = ...
```

Stop Gunicorn by pressing `Ctrl+C` or by writing in the terminal
```unix
$ pkill gunicorn
```

The recommended number of workers for an application running on a single production server is 
`number_of_CPU_cores * 2 + 1`.

The different workers have the different backend instances. 
This results in that the page visit counters in the Python code can alternate between each other.

## TOML = Tom's Obvious, Minimal Language

```unix
(venv) ... $ pip install dynaconf
```

The configuration information is stored in TOML files.

## Flask Debug Toolbar

That shows internal information right in the browser window.

https://github.com/pallets-eco/flask-debugtoolbar

```unix
(venv) ... $ pip install flask-debugtoolbar
```

The Flask Debug Toolbar requires the Flask app to have a `SECRET_KEY` value.
That can be generated using Python and must be not publicly available:

```python-console
$ python
>>> import secrets
>>> secrets.token_hex(24)
```

Copy the value into `.secrets.toml` as

```tolm
[default]
secret_key="..."
```

The `secret_key` is defined within the `[default]` section.
Its value is available in any other section unless it is overridden by another `secret_key` key-value pair.

The Flask Debug Toolbar also requires the creation of `settings.toml`. Only the information under `[default]` and the set environment will be
read from `settings.toml` at run time.

## Bootstrap (CSS framework)
https://getbootstrap.com/

## JSDELIVR (a free CDN for open source projects)
https://www.jsdelivr.com/

