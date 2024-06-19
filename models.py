from database import db

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'symbol': self.symbol}

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    indicator = db.Column(db.String(50), nullable=False)
    threshold = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'stock_id': self.stock_id, 'indicator': self.indicator, 'threshold': self.threshold}