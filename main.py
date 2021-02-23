import sys
import signal
from pprint import pprint
from mytrade import *


def write(message):
    sys.stdout.write(f'\r{message}')

d = myTradeStream.subscribe(write, pprint, pprint)

try:
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    while True:
        pass
except KeyboardInterrupt:
    d.dispose()
