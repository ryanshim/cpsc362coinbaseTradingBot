'''
Coinbase wallet authentication class
'''
import hmac, hashlib, time, requests, json

class CoinbaseWalletAuth():
    def __init__(self):
        self.api_key = b"API_KEY_HERE"
        self.secret_key = b"API_SECRET_HERE"


    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url + (request.body or '')
        signature = hmac.new(self.secret_key,
                             message.encode('utf-8'),
                             hashlib.sha256).hexdigest()
        vers_header = "2017-05-24" 
        request.headers.update({
                'CB-ACCESS-SIGN': signature,
                'CB-ACCESS-TIMESTAMP': timestamp,
                'CB-ACCESS-KEY': self.api_key,
                'CB-VERSION': vers_header,
            })
        return request
