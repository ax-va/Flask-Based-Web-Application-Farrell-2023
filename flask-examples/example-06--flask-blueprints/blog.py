from app import create_app

app = create_app()

# Open the directory in the terminal.
# Enter on Mac / Unix:
"""
$ export FLASK_ENV=development
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