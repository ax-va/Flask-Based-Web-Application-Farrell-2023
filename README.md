# Flask-Web-Application-Farrell-2023

## WSGI = Web Server Gateway Interface

Two of the most common production-ready high-performance WSGI servers are uWSGI and Gunicorn (short for Green Unicorn).

To run a Flask application using Gunicorn, you need to install it in the Python virtual environment with Flask:
```unix
(venv) ... $ pip install gunicorn
```

Run the webserver with four worker instances in a directory with 'xyz.py'
```unix
$ gunicorn -w 4 xyz:app
```


The first part, `xyz`, corresponds to the name of some 'xyz.py' script that is an entry point to the Flask application. Here, `xyz` is either `blog` or `app` depending on which example you have opened. The second part, `:app`, refers to the Flask application instance `app` created in the 'xyz.py' entry point:
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

## Flask settings

The Flask `app` must usually store a `SECRET_KEY` value.
That can be generated using Python and must be **not publicly** available:

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

Add `.secrets.toml` to `.gitignore`.

The Flask setting can be written in `settings.toml`. Only the information under `[default]` and the set environment will be read from `settings.toml` at run time.

In the settings, logging levels typically used are `DEBUG` (=10) for development and `INFO` (=20) for production.

## Flask sessions

Flask uses the `SECRET_KEY` to sign the session cookie.
The `SECRET_KEY` must be cryptographically strong and kept private on the server side.
That cookie is saved in the client's browser and cannot be modified by the client.

By default, session cookies exist until the client browser is closed but that livetime can be changed. 
The user information can be stored on the server side and retrieved using the session cookie's unique user identifier.

## Bootstrap (CSS framework)

https://getbootstrap.com/

## JSDELIVR 
A free CDN for open source projects

https://www.jsdelivr.com/

## Flask-Login
A Flask extension to provide application session management abilities and tools to log users in and out and handle the "remember me" functionality.

https://pypi.org/project/Flask-Login/

https://flask-login.readthedocs.io/en/latest/

## Flask-WTF
Simple integration of Flask and WTForms, including cross-site request forgery (CSRF) protection, file upload, and reCAPTCHA.

https://pypi.org/project/Flask-WTF/

## Flask-Bcrypt
A Flask extension to hash the passwords stored on the server. 
Plain-text passwords should never be stored in a database and should always be cryptographically hashed first.

https://pypi.org/project/Flask-Bcrypt/

https://snyk.io/advisor/python/flask-bcrypt

https://pypi.org/project/bcrypt/

## Test users

| Fake email                | Password |
|---------------------------|----------|
| `ax-va@email.com`         | `secret` |
| `johnny-depp@email.com`   | `123456` |
| `alex-alex@email.com`     | `123456` |


## Conformation by email with Brevo (earlier SendInBlue)

https://www.brevo.com/de/pricing/

Server-side API client:

https://developers.brevo.com/docs/api-clients

https://github.com/sendinblue/APIv3-python-library

```unix
(venv) ... $ pip install sib-api-v3-sdk
```

Generate an API Key

https://app.brevo.com/settings/keys/api

to add it to .secrets.tolm
```tolm
sib_api_key = 'xkeysib-...'
```
