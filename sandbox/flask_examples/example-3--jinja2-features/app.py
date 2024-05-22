import json
from typing import List

from flask import Flask, render_template
from datetime import datetime
from random import sample

app = Flask(__name__)


class PageVisit:
    """ Counts the visits of the web page """
    VISITS = 0

    @classmethod
    def increment_visits(cls) -> int:
        cls.VISITS += 1
        return cls.VISITS


class BannerColors:
    """ Chooses randomly 5 colors from the colors that are CSS-valid and available in the class """
    COLORS = [
        'aqua',
        'blue',
        'darkcyan',
        'darkkhaki',
        'firebrick',
        'gold',
        'gray',
        'green',
        'greenyellow',
        'indigo',
        'khaki',
        'lightcoral',
        'lime',
        'olive',
        'pink',
        'purple',
        'red',
        'salmon',
        'sienna',
        'silver',
        'skyblue',
        'tan',
        'violet',
        'yellow',
    ]

    @staticmethod
    def get_colors() -> List[str]:
        """ Returns randomly 5 colors """
        return sample(BannerColors.COLORS, 5)


@app.route("/")
def home():
    banner_colors = BannerColors.get_colors()
    return render_template(
        "index.html",
        data={
            "now": datetime.now(),
            "page_visit": PageVisit(),
            "banner_colors": banner_colors,
        }
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