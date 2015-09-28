#! /usr/bin/python3

import time
from datetime import datetime
import requests
import json
from daemon.Daemon import Daemon

class RateDetector(Daemon):
    url = "https://transferwise.com/request/initiatePageRate"
    payload = {
    'calculatorView': 1, 
    'lang': 'en', 
    'fixType': 'SOURCE',
    'hideSavings': 'true',
    'signup': 'true',
    'p.fromCalcWidget': 'true',
    'p.sourceAmount': 5000,
    }
# 3 = USD / 1 = EUR / 2 = GBP
    def startCollection(self,amount,sourceCurrency=3,targetCurrency=1):
        status = 200
        start = datetime.now()
        lastSum = 0.00001;
        while status == 200 :
            time.sleep(2)
            now = datetime.now()
            self.payload["sourceValue"] = amount
            self.payload["sourceCurrencyId"] = sourceCurrency
            self.payload["targetCurrencyId"] = targetCurrency
            r = requests.post(self.url, data=self.payload)
            status = r.status_code
            rj = json.loads(r.text)
            euro = float(rj['targetValue'].replace(',',''))
            doll = float(rj['sourceValue'].replace(',',''))
            fee = rj['fee']
            delta = abs(lastSum-euro)/(lastSum)
            if delta>0.0002 and doll>0:
                lastSum = euro
                print(euro,euro/doll,now,fee)
    def run(self):
        self.startCollection(5000)

