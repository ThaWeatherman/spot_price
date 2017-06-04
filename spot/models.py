from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Commodity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    value = db.Column(db.Float)

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '<Commodity({}, {})>'.format(self.name, self.value)


class LastCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last = db.Column(db.DateTime)

    def __init__(self, last):
        self.last = last

    def __repr__(self):
        return '<LastCheck({})>'.format(str(self.last))

