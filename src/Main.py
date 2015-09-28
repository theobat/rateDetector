#! /usr/bin/python3

import sys
from RateDetector import RateDetector

if __name__ == "__main__":
    pidfile="/tmp/daemon-example.pid"
    outfile="/home/batoz/project/rateDetector/output"
    errfile="/home/batoz/project/rateDetector/errfile"
    daemon = RateDetector(pidfile, stdout=outfile,stderr=errfile)
    #daemon.startCollection(5000)
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
