import sqlite3
from database import get_db_connection

class Alert():
    id = 0
    stock_id = 0
    indicator = ''
    threshold = 0.0

    def to_dict(self):
        return {
            "id": self.id,
            "stock_id": self.stock_id,
            "indicator": self.indicator,
            "threshold": self.threshold,
        }
