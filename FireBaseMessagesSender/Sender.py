from pyfcm import FCMNotification

API_KEY = 'AAAA1aUCkXI:APA91bE4dLTjccZ9hvH37UA15rALZParqHrCFEF6LzuQnsJSUWJXRfGV' \
          '-KV5xeK2NwSER5CIDhbL6X1jhSNLX7bpdzY5cR5z60zbXTR8ihvIDEZfU3pH7TMkU0QH8tVLRFl6sa4rAHDN '
TOPIC_NEWS = 'news'


class Sender:

    def __init__(self):
        '''
        Constructor
        '''
        self.push_service = FCMNotification(api_key=API_KEY)

    def send_message(self, market=""):
        result = self.push_service.notify_topic_subscribers(topic_name=TOPIC_NEWS, message_title='first_try', message_body='from server!', data_message={'laal':'dada'})

        print(result)
