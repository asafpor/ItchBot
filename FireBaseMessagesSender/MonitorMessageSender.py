from pyfcm import FCMNotification
from Currency import Currency
from datetime import datetime
import json

API_KEY = 'AAAA1aUCkXI:APA91bE4dLTjccZ9hvH37UA15rALZParqHrCFEF6LzuQnsJSUWJXRfGV-KV5xeK2NwSER5CIDhbL6X1jhSNLX7bpdzY5cR5z60zbXTR8ihvIDEZfU3pH7TMkU0QH8tVLRFl6sa4rAHDN '
TOPIC_NEWS = 'news'
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TITLE_ACCOUNT_BALANCE = "Account balance update"
TYPE_ACCOUNT_BALANCE = "account_balance"


class MonitorMessageSender:

    def __init__(self):
        '''
        Constructor
        '''
        self.__push_service = FCMNotification(api_key=API_KEY)

    def send_account_balance(self, btc, usd, currencies=[], market="Bittrex"):
        coins = []
        for coin in currencies:
            if not isinstance(coin, Currency):
                raise Exception('illegal variable currencies, use array of Currency')
            coins.append(coin.to_json())
        message_data = {'btc': btc, 'usd': usd, "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'currencies': coins, "market": market}
        print(message_data)
        result = self.__push_service.notify_topic_subscribers(topic_name=TOPIC_NEWS,
                                                              message_title=TITLE_ACCOUNT_BALANCE,
                                                              tag=TYPE_ACCOUNT_BALANCE,
                                                              data_message=message_data)
        print(result)
