from flask import Flask, render_template  # render_template for using Jinja2
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route("/")
def home():
    current_time = datetime.now().strftime('%H:%M:%S.%f')
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    return render_template(
        "index.html",
        current_time=current_time,
        today=today,
        yesterday=yesterday,
    )


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

# Open in the browser
# http://127.0.0.1:5000/
"""
127.0.0.1 - - [20/May/2024 21:14:48] "GET / HTTP/1.1" 200 -
"""
# Refresh the web page.
