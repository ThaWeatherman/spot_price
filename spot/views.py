from flask import Blueprint, render_template

from .models import Commodity, LastCheck


main = Blueprint('main', __name__)


@main.route('/')
def index():
    commodities = Commodity.query.all()
    last = LastCheck.query.get(1)
    prices = {'last': str(last.last)}
    for commodity in commodities:
        prices[commodity.name] = commodity.value
    return render_template('index.html', prices=prices)

