from flask import Flask
from flask_restful import Resource, Api

from .models import db, Commodity, LastCheck
from .views import main


api = Api()


def create_app(debug=True):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = debug
    db.init_app(app)
    api.init_app(app)
    app.register_blueprint(main)
    return app


class CommodityResource(Resource):
    def get(self, commodity):
        last = LastCheck.query.get(1)
        last = str(last.last)
        c = Commodity.query.filter_by(name=commodity).first()
        if c is not None:
            return {commodity: c.value, 'last': last}
        elif commodity == 'all':
            commodities = Commodity.query.all()
            d = {'last': last}
            for commodity in commodities:
                d[commodity.name] = commodity.value
            return d
        else:
            return {'error': 'No such commodity'}, 400


api.add_resource(CommodityResource, '/api/<string:commodity>')

