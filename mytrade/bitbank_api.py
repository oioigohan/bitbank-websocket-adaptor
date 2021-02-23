import pickle
import requests
import python_bitbankcc
from typing import List
from dataclasses import dataclass
from python_bitbankcc.utils import error_parser
from .bitbank_models import *
from mytrade.parameters import PAIR


class bitbank_public(python_bitbankcc.public):

    def __init__(self):
        super().__init__()
        self.end_point2 = 'https://api.bitbank.cc'

    def get_status(self):
        path = '/v1/spot/status'
        return self._query2(self.end_point2 + path)

    def get_pairs(self):
        path = '/v1/spot/pairs'
        return self._query2(self.end_point2 + path)

    def _query2(self, query_url):
        response = requests.get(query_url)
        return error_parser(response.json())


class BitBankAPI():

    def __init__(self, pair=PAIR):

        # プライベートなWebAPIメソッドの仕様にはAPIキーとSecretが必要

        #     1. ファイルから読み込む
        #     with open('<file-path-to-your-api-key>', 'rb') as f:
        #         key = pickle.load(f)
        #
        #     apiKey = key['apiKey']
        #     secret = key['secret']

        #     2. コマンドラインから入力する
        #     apiKey = input('apiKeyを入力してください。\n> ')
        #     secret = input('secretを入力してください。\n> ')

        #     3. プライベートなメソッドを使用しない
        apiKey =''
        secret = ''

        self.pub = bitbank_public()
        self.prv = python_bitbankcc.private(apiKey, secret)
        self.pair = pair

    # public WebAPI methods

    def ticker(self, _=None) -> Ticker:
        res = self.pub.get_ticker(self.pair)
        return Ticker.from_dict(res)

    def depth(self, _=None) -> DepthWhole:
        res = self.pub.get_depth(self.pair)
        return DepthWhole.from_dict(res)

    def transactions(self, day: int = None) -> TransactionsData:
        res = self.pub.get_transactions(self.pair, day)
        return TransactionsData.from_dict(res)

    def candlestick(self, day, type: str = '1hour') -> CandleStickData:
        res = self.pub.get_candlestick(self.pair, type, day)
        return CandleStickData.from_dict(res)

    def statuses(self, _=None) -> StatusesData:
        res = self.pub.get_status()
        return StatusesData.from_dict(res)

    def pairs(self, _=None) -> PairsData:
        res = self.pub.get_pairs()
        return PairsData.from_dict(res)

    # private WebAPI methods

    def assets(self, _=None):
        res = self.prv.get_asset()
        return AssetsData.from_dict(res)

    def get_order(self, order_id: int) -> Order:
        res = self.prv.get_order(self.pair, order_id)
        return Order.from_dict(res)

    def order(self, price: float, amount: float, side: str, order_type: str) -> Order:
        res = self.prv.order(self.pair, price, amount, side, order_type)
        return Order.from_dict(res)

    def cancel_order(self, order_id: int) -> Order:
        res = self.prv.cancel_order(self.pair, order_id)
        return Order.from_dict(res)

    def cancel_orders(self, order_ids: List[int]) -> OrdersData:
        res = self.prv.cancel_orders(self.pair, order_ids)
        return OrdersData.from_dict(res)

    def get_orders_info(self, order_ids: List[int]) -> OrdersData:
        res = self.prv.get_orders_info(self.pair, order_ids)
        return OrdersData.from_dict(res)

    def get_active_orders(self, options=None) -> OrdersData:
        res = self.prv.get_active_orders(self.pair, options)
        return OrdersData.from_dict(res)

    def get_trade_history(self, order_count=10) -> TradesData:
        res = self.prv.get_trade_history(self.pair, order_count)
        return TradesData.from_dict(res)

    def get_withdraw_account(self, asset='jpy') -> AccountsData:
        res = self.prv.get_withdraw_account(asset)
        return AccountsData.from_dict(res)

    def request_withdraw(self, asset, uuid, amount, token):
        return self.prv.request_withdraw(asset, uuid, amount, token)
