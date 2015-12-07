import atexit
import re
import threading

from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template
from flask_restful import Resource, Api
import requests


PRICES = {}
THREAD = threading.Thread()
LOCK = threading.Lock()
SLEEP = 5


def create_app():
    app = Flask(__name__)

    def interrupt():
        global THREAD
        THREAD.cancel()

    def get_prices():
        global PRICES
        global THREAD
        req = requests.get('http://www.apmex.com')
        soup = BeautifulSoup(req.content, 'lxml')
        table = soup.select('table.table-spot-prices')[0]
        # column order: metal, bid, ask, change
        # metal order: gold, silver, platinum, palladium
        rows = table.find_all('tr')
        prices = [row.find_all('td')[2] for row in rows[1:]]  # 2 is ask
        with LOCK:
            PRICES = {'gold': prices[0].text, 'silver': prices[1].text,
                      'platinum': prices[2].text, 'palladium': prices[3].text}
            for metal in PRICES:
                PRICES[metal] = re.sub(r'[^\d.]', '', PRICES[metal])
        THREAD = threading.Timer(SLEEP, get_prices, ())
        THREAD.start()

    def start():
        global THREAD
        THREAD = threading.Timer(SLEEP, get_prices, ())
        THREAD.start()

    start()
    atexit.register(interrupt)
    return app


app = create_app()
api = Api(app)


class Gold(Resource):
    def get(self):
        return {'gold': PRICES['gold']}


class Silver(Resource):
    def get(self):
        return {'silver': PRICES['silver']}


class Platinum(Resource):
    def get(self):
        return {'platinum': PRICES['platinum']}


class Palladium(Resource):
    def get(self):
        return {'palladium': PRICES['palladium']}


class All(Resource):
    def get(self):
        return PRICES


api.add_resource(Gold, '/api/gold')
api.add_resource(Silver, '/api/silver')
api.add_resource(Platinum, '/api/platinum')
api.add_resource(Palladium, '/api/palladium')
api.add_resource(All, '/api/all')


@app.route('/')
def index():
    return render_template('index.html', prices=PRICES)

if __name__ == '__main__':
    app.run(debug=True)
