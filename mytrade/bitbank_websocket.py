import json
import websocket
from sys import stdout as std
from time import sleep
from threading import Thread
from rx.subject import Subject


class BitBankWebSocket(Subject):

    _url_ = 'wss://stream.bitbank.cc/socket.io/?transport=websocket'
    _write_ = lambda message: std.write(f'\r{message}')

    @property
    def is_connected(self):
        return bool(self.ws.sock and self.ws.sock.connected)

    def __init__(self, channel, / , url=_url_):
        super().__init__()
        self.url = url
        self.channel = channel
        self.ws = websocket.WebSocketApp(
            url=self.url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close)

    def connect(self):
        self.ws.keep_running = True
        self.thread = Thread(target=lambda: self.ws.run_forever())
        self.thread.daemon = True
        self.thread.start()

    def disconnect(self):
        self.ws.keep_running = False
        self.ws.close()

    def easy_subscribe(self, sec=10, next=_write_):
        self.connect()
        d = self.subscribe(next)
        sleep(sec)
        d.dispose()
        self.disconnect()

    def _on_open(self):
        params = f'42["join-room","{self.channel}"]'
        self.ws.send(params)

    def _on_message(self, message):
        self.on_next(message)

    def _on_error(self, error):
        self.disconnect()
        self.connect()

    def _on_close(self):
        # self.on_completed()
        pass


class Channels():

    @property
    def ticker(self):
        return f'ticker_{self.pair}'

    @property
    def transactions(self):
        return f'transactions_{self.pair}'

    @property
    def depth_diff(self):
        return f'depth_diff_{self.pair}'

    @property
    def depth_whole(self):
        return f'depth_whole_{self.pair}'

    def __init__(self, pair='btc_jpy'):
        self.pair = pair
