#! /usr/bin/python
import sys
import time
import datetime
import requests
import json
from daemon.Daemon import Daemon

class MyDaemon(Daemon):
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
        start = datetime.datetime.now()
        while status == 200 :
            time.sleep(2)
            now = datetime.datetime.now()
            delta = now-start
            self.payload["sourceValue"] = amount
            self.payload["sourceCurrencyId"] = sourceCurrency
            self.payload["targetCurrencyId"] = targetCurrency
            r = requests.post(self.url, data=self.payload)
            status = r.status_code
            rj = json.loads(r.text)
            euro = float(str.replace(rj['targetValue'],',',''))
            doll = float(str.replace(rj['sourceValue'],',',''))
            print(euro,rj['fee'])
            print(euro/doll,delta)
    def run(self):
        self.startCollection()

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-example.pid')
    daemon.startCollection(5000)
    if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                    daemon.start()
            elif 'stop' == sys.argv[1]:
                    daemon.stop()
            elif 'restart' == sys.argv[1]:
                    daemon.restart()
            else:
                    print("Unknown command")
                    sys.exit(2)
            sys.exit(0)
    else:
            print("usage: %s start|stop|restart" % sys.argv[0])
            sys.exit(2)
