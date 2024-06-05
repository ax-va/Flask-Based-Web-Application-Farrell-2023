# Python-Web-Application-Farrell-2023

## WSGI

Two of the most common production-ready high-performance WSGI servers are uWSGI and Gunicorn (short for Green Unicorn).

To run a Flask application using Gunicorn, you need to install it in the Python virtual environment with Flask:
```unix
(venv) ... $ pip install gunicorn
```

Run the webserver with four worker instances in a directory with 'app.py' / 'blog.py'
```unix
$ gunicorn -w 4 app:app
```
```unix
$ gunicorn -w 4 blog:app
```
The first part, `app` / `blog`, corresponds to 'app.py' / 'blog.py', respectively. The second part, `:app`, refers to the Flask application instance created in 'app.py' or 'blog.py':
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

Logging levels typically used are DEBUG (=10) for development and INFO (=20) for production.

## Flask sessions

Flask uses the `SECRET_KEY` to sign the session cookie.
The `SECRET_KEY` must be cryptographically strong and kept private on the server side.
That cookie is saved in the client's browser and cannot be modified by the client.

By default, session cookies exist until the client browser is closed that can be changed using Python `datetime.timedelta()`. 
The user information can be stored on the server side and retrieved using the session cookie's unique user identifier.

## Bootstrap (CSS framework)

https://getbootstrap.com/

## JSDELIVR (a free CDN for open source projects)

https://www.jsdelivr.com/

## Flask-Login
A Flask extension to provide application session management abilities and tools to log users in and out and handle the "remember me" functionality.

https://pypi.org/project/Flask-Login/

## Flask-Bcrypt
A Flask extension to hash the passwords stored on the server

https://pypi.org/project/Flask-Bcrypt/

https://snyk.io/advisor/python/flask-bcrypt
