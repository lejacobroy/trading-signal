import sqlite3

class Alert():
    def __init__(self, id=None, stock_id=None, indicator_id=None, period_id=None, interval_id=None, action=None, threshold=None):
        self.id = id
        self.stock_id = stock_id
        self.indicator_id = indicator_id
        self.period_id = period_id
        self.interval_id = interval_id
        self.action = action
        self.threshold = threshold
        
    def to_dict(self):
        return {
            "id": self.id,
            "stock_id": self.stock_id,
            "indicator_id": self.indicator_id,
            "period_id": self.period_id,
            "interval_id": self.interval_id,
            "action": self.action,
            "threshold": self.threshold,
        }
