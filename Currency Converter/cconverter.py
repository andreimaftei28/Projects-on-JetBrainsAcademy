import requests
import json

cache = {}
currency_code = input().lower()
url = f"http://www.floatrates.com/daily/{currency_code}.json"
data = requests.get(url)
currency = json.loads(data.text)
if currency_code != 'usd':
    cache['usd'] = currency['usd']
if currency_code != 'eur':
    cache['eur'] = currency['eur']
while True:
    exch_currency = input().lower()
    if exch_currency != "":
        try:
            money = float(input())
            if exch_currency in cache:
                print(f"Checking the cache…\nOh! It is in the cache!\nYou received {round(money * currency[exch_currency]['rate'], 2)} {exch_currency.upper()}")
            else:
                url = f"http://www.floatrates.com/daily/{currency_code}.json"
                data = requests.get(url)
                currency = json.loads(data.text)
                cache[exch_currency] = currency[exch_currency]

                print(f"Checking the cache…\nSorry, but it is not in the cache!\nYou received {round(money * currency[exch_currency]['rate'], 2)} {exch_currency.upper()}")
        except ValueError:
            break
    else:
        break


