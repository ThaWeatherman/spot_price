import atexit
import datetime
import threading

from flask import Flask
from flask import render_template
from flask_restful import Resource, Api
import requests


PRICES = {}
THREAD = threading.Thread()
LOCK = threading.Lock()
SLEEP = 60


def create_app():
    app = Flask(__name__)

    def interrupt():
        global THREAD
        THREAD.cancel()

    def get_prices():
        global PRICES
        global THREAD
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        while True:
            try:
                req = requests.get('http://www.providentmetals.com/services/spot/summary.USD.json', headers=headers)
                if req.status_code == 200:
                    break
            except:
                continue
        try:
            # bitfinex ltc: https://api.bitfinex.com/v1/pubticker/ltcusd
            ltc_price = round(float(requests.get("https://api.kraken.com/0/public/Ticker?pair=xltczusd").json()['result']['XLTCZUSD']['b'][0]), 2)
            btc_price = float(requests.get('https://api.coinbase.com/v2/prices/spot?currency=USD').json()['data']['amount'])# btc()
        except Exception:
            ltc_price = PRICES['litecoin'] if 'litecoin' in PRICES else 0
            btc_price = PRICES['bitcoin'] if 'bitcoin' in PRICES else 0
        try:
            now = str(datetime.datetime.utcnow())
            with LOCK:
                PRICES = {metal['metal_desc'].lower():metal['rate'] for metal in req.json()}
                for metal in PRICES:
                    PRICES[metal] = round(float(PRICES[metal]), 2)
                PRICES['last'] = now
                PRICES['bitcoin'] = btc_price
                PRICES['litecoin'] = ltc_price
        except Exception as e:
            print(str(e))
        finally:
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


class Metal(Resource):
    def get(self, metal):
        if metal in PRICES:
            return {metal: PRICES[metal], 'last': PRICES['last']}
        elif metal == 'all':
            return PRICES
        else:
            return {'error': 'No such metal'}, 400


api.add_resource(Metal, '/api/<string:metal>')


@app.route('/')
def index():
    return render_template('index.html', prices=PRICES)

if __name__ == '__main__':
    app.run(debug=True)
