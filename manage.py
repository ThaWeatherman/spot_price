import datetime

import bs4
from flask_script import Manager
import requests

from spot import create_app, db
from spot.models import Commodity, LastCheck


app = create_app()
manager = Manager(app)


@manager.command
def create_db():
    db.create_all()


@manager.command
def update_prices():
    prices = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    while True:
        try:
            req = requests.get('https://www.providentmetals.com/wp-content/themes/provident/includes/current-spot.php', headers=headers)
            if req.status_code == 200:
                break
            else:
                print(req.status_code)
        except:
            continue
    # prices = {metal['metal_desc'].lower():metal['rate'] for metal in req.json()}
    soup = bs4.BeautifulSoup(req.content, 'lxml')
    li = soup.ul.findAll("li")
    li = li[:4]  # MAGIC NUMBER ALERT, periodically check back to ensure this is correct
    for l in li:
        sp = l.findAll("span")
        prices[sp[0].text] = sp[1].text.replace('$', '').replace(',', '')
    # bitfinex ltc: https://api.bitfinex.com/v1/pubticker/ltcusd
    # ltc_price = round(float(requests.get("https://api.kraken.com/0/public/Ticker?pair=xltczusd").json()['result']['XLTCZUSD']['b'][0]), 2)
    ltc_price = float(requests.get('https://api.coinbase.com/v2/prices/LTC-USD/spot').json()['data']['amount'])
    btc_price = float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot').json()['data']['amount'])
    eth_price = float(requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot').json()['data']['amount'])
    now = datetime.datetime.utcnow()
    for metal in prices:
        prices[metal] = round(float(prices[metal]), 2)
    last = LastCheck.query.get(1)
    if last is None:
        last = LastCheck(now)
    else:
        last.last = now
    db.session.add(last)
    db.session.commit()
    prices['bitcoin'] = btc_price
    prices['litecoin'] = ltc_price
    prices['ethereum'] = eth_price
    for metal in prices:
        c = Commodity.query.filter_by(name=metal).first()
        if c is None:
            c = Commodity(metal, prices[metal])
        else:
            c.value = prices[metal]
        db.session.add(c)
    db.session.commit()


if __name__ == '__main__':
    manager.run()

