# Import libraries
from pyquery import PyQuery as pq
import requests
import json
import urllib
from functools import reduce
from time import time
def plus(x, y):
    return x + y
# Telegram receiver information
TOKEN = "5569312879:AAFh1Si470K5zKIiv91c74JfcSg76hQ2w2E" 
chat_id = "1309473750"  

# download document from the api of XRP price in kraken
timestamp = int(time()) - (5 * 60)
data_text = pq(url='https://api.kraken.com/0/public/Trades?pair=XRPUSD&since=' + str(timestamp))

# turn the document into JSON
data_json = json.loads(data_text.text())
btc_usd_trades = data_json['result']['XXRPZUSD']
# trade[0] is price
# trade[1] is amount
sum_weighted_price = reduce(plus, [float(trade[0]) * float(trade[1]) for trade in btc_usd_trades])
sum_amount = reduce(plus, [float(trade[1]) for trade in btc_usd_trades])

# XRP / USD in Kraken

xrpusd_kraken = round(sum_weighted_price/sum_amount, 5)


# XRP / KRW price in UPBIT
data_text = pq(url='https://api.upbit.com/v1/ticker?markets=KRW-XRP')
data_json = json.loads(data_text.text())
krwxrp_upbit = data_json[0]['trade_price']
print(krwxrp_upbit)
# KRW-USD FX rate 
url_fx_data = "https://api.apilayer.com/exchangerates_data/convert?to=KRW&from=USD&amount=1"

payload = {}
headers= {
  "apikey": "9PeUjkugDrfmElNqFxKkKAXVZ0gpBMm7"
}

response = requests.request("GET", url_fx_data, headers=headers, data = payload)

# FX rate data is taken out
status_code = response.status_code
result = response.text
fx_data = result.split()

krwusd = round(float(fx_data[17]),5)

# XRP / USD price in UPBIT

xrpusd_upbit = round(krwxrp_upbit / krwusd,5)

# Kimchi Premium

kimchi_p = round(1 + (xrpusd_upbit-xrpusd_kraken) / xrpusd_kraken, 5)

message = str('XRP price in Kraken'), xrpusd_kraken, str('XRP / USD price in Upbit '), xrpusd_upbit, str( 'Kimchi_P'), kimchi_p

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
print(requests.get(url).json()) # this sends the message