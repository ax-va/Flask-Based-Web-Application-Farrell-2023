from flask import Flask
from app import create_app

app: Flask = create_app()
app.logger.info("AlexBlog is running")

# Open the directory in the terminal.
# Enter on Mac / Unix:
"""
$ export FLASK_ENV=development
"""
# By default, Flask looks for the Flask "app" instance in the "FLASK_APP" environment variable
"""
$ export FLASK_APP=blog.py
"""

# Enter on Windows:
"""
> set FLASK_ENV=development
> set FLASK_APP=blog.py
"""

# Then, run the Flask built-in web server
"""
$ flask run
 * Serving Flask app 'blog.py'
 * Debug mode: off
[2024-06-02 16:02:32.046]INFO in _internal: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
[2024-06-02 16:02:32.046]INFO in _internal: Press CTRL+C to quit
"""
# !
# - The web server is running in development mode, which isn't suitable for production.
# - The Flask built-in development server isn't optimized or secure enough to be used out in the wild.
# - The server is in an idle state waiting to receive and process HTTP requests.
# - The Flask development server defaults to running at IP address 127.0.0.1 on port 5000.
# - The IP address 127.0.0.1 is known as localhost.

# Open in the browser
# http://127.0.0.1:5000/
"""
[2024-06-02 16:03:36.100]DEBUG in home: Rendering the 'home' page...
[2024-06-02 16:03:36.177]INFO in _internal: 127.0.0.1 - - [02/Jun/2024 16:03:36] "GET / HTTP/1.1" 200 -
...
[2024-06-02 16:05:09.302]DEBUG in about: Rendering the 'about' page...
"""

# To don't log the DEBUG messages, set "FLASK_ENV=production" instead of "FLASK_ENV=development".

# Credentials of test users:
# 1. ax-va@email.com secret
# 2. johnny-depp@email.com 123456
# 3. alex-alex@email.com 123456