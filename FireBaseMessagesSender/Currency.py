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
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
