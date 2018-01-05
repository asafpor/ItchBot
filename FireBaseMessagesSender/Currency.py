import json


class Currency:
    def __init__(self, name, symbol, available_balance, pending_deposit, reserved, total, est_btc_val, change_pct):
        '''
        Constructor
        '''
        self.name = name
        self.symbol = symbol
        self.available_balance = available_balance
        self.pending = pending_deposit
        self.reserved = reserved
        self.total = total
        self.est_btc_val = est_btc_val
        self.change_pct = change_pct

    def to_json(self):
        return json.dumps({"name": self.name,
                           "symbol": self.symbol,
                           "available_balance": self.available_balance,
                           "pending": self.pending,
                           "reserved": self.reserved,
                           "est_btc_val": self.est_btc_val,
                           "change_pct": self.change_pct,
                           "total": self.total})
