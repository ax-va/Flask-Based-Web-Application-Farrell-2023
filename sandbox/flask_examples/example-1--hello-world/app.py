from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    # To create a proper web page, the server should return a string with an HTML code
    return "Hello World!"


# Open the directory in the terminal.
# Enter on Mac / Unix:
"""
$ export FLASK_ENV=development
$ export FLASK_APP=app.py
"""

# Enter on Windows:
"""
> set FLASK_ENV=development
> set FLASK_APP=app.py
"""

# Then
"""
$ flask run
 * Serving Flask app 'app.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
"""
# !
# - The web server is running in development mode, which isn't suitable for production.
# - The Flask built-in development server isn't optimized or secure enough to be used out in the wild.
# - The server is in an idle state waiting to receive and process HTTP requests.
# - The Flask development server defaults to running at IP address 127.0.0.1 on port 5000.
# - The IP address 127.0.0.1 is known as localhost.

# Open in the browser to see "Hello World!"
# http://127.0.0.1:5000/
"""
127.0.0.1 - - [20/May/2024 19:21:48] "GET / HTTP/1.1" 200 -
"""

# Try to open http://127.0.0.1:5000/something
"""
127.0.0.1 - - [20/May/2024 19:30:07] "GET /something HTTP/1.1" 404 -
"""
# 404 denotes "Page Not Found"
