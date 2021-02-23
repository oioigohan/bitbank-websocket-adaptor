import rx
import json
import threading
import rx.operators as ops
from time import sleep
from typing import List
from datetime import datetime
from .bitbank_api import BitBankAPI, StatusType
from .bitbank_websocket import BitBankWebSocket, Channels
from .bitbank_models import *
from mytrade.parameters import PAIR, AMOUNT, SOCKET_LIMIT_SEC, \
    ALPHA, BETA

ch = Channels(PAIR)
bitbank = BitBankAPI(PAIR)


# bitbankのWebSocketは30秒で接続が切断される仕様のため
# 繰り返し接続を行い情報を継続的に取得できる次のようなstreamを考える
#
# 20秒毎に新しいstreamを作る
# streamが作られると同時に接続を開始(制限時間はこの時点から30秒)
# 27秒後に接続を切断するように設定
# 接続完了までの5秒間はstreamを返さない
#
# 0sec-=----10---=----20---=----30---=----40---=----50---=----60---=----70->
# o-------------------o-------------------o-------------------o------------>
# L----c=====================x--|
#                     L----c=====================x--|
#                                         L----c=====================x--|
#
#                           ↓↓↓ switch_latest ↓↓↓
#
# s----c===================================================================>

def temporarySocket(channel):
    stream = BitBankWebSocket(channel)
    stream.connect()
    threading.Timer(SOCKET_LIMIT_SEC-3, stream.disconnect).start()
    sleep(5)
    return stream


def sequentialSocket(channel):
    scheduler = rx.scheduler.timeoutscheduler.TimeoutScheduler()
    stream = rx.interval(SOCKET_LIMIT_SEC-10, scheduler).pipe(
        ops.start_with('start'),
        ops.map(lambda _: temporarySocket(channel)),
        ops.switch_latest(),
        ops.filter(lambda res: res[:2] == '42'),
        ops.map(lambda res: json.loads(res[13:-1])),
        ops.map(Response.from_dict),
        ops.map(lambda res: res.message.data),
    )
    return stream


# Upstream

# WebSocket

tickerSocket = sequentialSocket(ch.ticker)
transactionsSocket = sequentialSocket(ch.transactions)
depthDiffSocket = sequentialSocket(ch.depth_diff)
depthWholeSocket = sequentialSocket(ch.depth_whole)

tickerStream = tickerSocket.pipe(ops.map(Ticker.from_dict))
transactionsStream = transactionsSocket.pipe(
    ops.map(TransactionsData.from_dict))
depthDiffStream = depthDiffSocket.pipe(ops.map(DepthDiff.from_dict))
depthWholeStream = depthWholeSocket.pipe(ops.map(DepthWhole.from_dict))


# API

clockStream = rx.interval(10).pipe(ops.start_with('start'))

# Public

tickerAPI = clockStream.pipe(ops.map(bitbank.ticker))
depthAPI = clockStream.pipe(ops.map(bitbank.depth))
transactionsAPI = clockStream.pipe(ops.map(bitbank.transactions))
candlestickAPI = clockStream.pipe(ops.map(bitbank.candlestick))
statusesAPI = clockStream.pipe(ops.map(bitbank.statuses))
pairsAPI = clockStream.pipe(ops.map(bitbank.pairs))

# Private

assetsAPI = clockStream.pipe(ops.map(bitbank.assets))
orderAPI = clockStream.pipe(ops.map(bitbank.order))
cancelOrderAPI = clockStream.pipe(ops.map(bitbank.cancel_order))
cancelOrdersAPI = clockStream.pipe(ops.map(bitbank.cancel_orders))
ordersInfoAPI = clockStream.pipe(ops.map(bitbank.get_orders_info))
activeOrdersAPI = clockStream.pipe(ops.map(bitbank.get_active_orders))
tradeHistoryAPI = clockStream.pipe(ops.map(bitbank.get_trade_history))
withdrawalAccountAPI = clockStream.pipe(ops.map(bitbank.get_withdraw_account))
requestWithdrawalAPI = clockStream.pipe(ops.map(bitbank.request_withdraw))

# MidStream

statusStream = statusesAPI.pipe(
    ops.map(lambda res: list(filter(lambda x: x.pair == PAIR, res.statuses))),
    ops.filter(bool),
    ops.map(lambda s: s[0]))

isHealthyStream = statusStream.pipe(
    ops.map(lambda s: s.status.upper() in (StatusType.NORMAL, StatusType.BUSY)))

assetStream = assetsAPI.pipe(
    ops.map(lambda res: list(filter(lambda x: x.asset == 'jpy', res.assets))),
    ops.filter(bool),
    ops.map(lambda a: a[0]))

hasEnoughCollateralStream = assetStream.pipe(
    ops.map(lambda a: float(a.locked_amount) / float(a.onhand_amount)),
    ops.map(lambda use_rate: use_rate < 0.5),)

canOrderStream = rx.zip(
    isHealthyStream, hasEnoughCollateralStream).pipe(
    ops.map(all),)

PriceLastBuyStream = transactionsStream.pipe(
    ops.map(lambda res: res.transactions),
    ops.map(lambda ts: list(filter(lambda x: x.side == 'buy', ts))),
    ops.filter(bool),
    ops.map(lambda ts: sorted(ts, key=lambda x: x.executed_at)),
    ops.map(lambda ts: ts[-1].price),)

PriceLastSellStream = transactionsStream.pipe(
    ops.map(lambda res: res.transactions),
    ops.map(lambda ts: list(filter(lambda x: x.side == 'sell', ts))),
    ops.filter(bool),
    ops.map(lambda ts: sorted(ts, key=lambda x: x.executed_at)),
    ops.map(lambda ts: ts[-1].price),)

# 10秒毎
PriceMinAskStream = depthWholeStream.pipe(
    ops.map(lambda res: res.asks),
    ops.filter(bool),
    ops.map(lambda ds: sorted(ds, key=lambda x: float(x[0]))),
    ops.map(lambda ds: float(ds[0][0])),)

# 10秒毎
PriceMaxBidStream = depthWholeStream.pipe(
    ops.map(lambda res: res.bids),
    ops.filter(bool),
    ops.map(lambda ds: sorted(ds, key=lambda x: float(x[0]))),
    ops.map(lambda ds: float(ds[-1][0])),)


def buy(price, amount=AMOUNT):
    return bitbank.order(price, amount, 'buy', 'limit')


def sell(price, amount=AMOUNT):
    return bitbank.order(price, amount, 'sell', 'limit')


priceBuyMainStream = rx.combine_latest(
    PriceLastSellStream, PriceMaxBidStream).pipe(
    ops.map(lambda ps: (float(ps[0]) + float(ps[1])) / 2))

priceBuyLCStream = priceBuyMainStream.pipe(
    ops.map(lambda p: p + ALPHA))

priceSellMainStream = rx.combine_latest(
    PriceLastBuyStream, PriceMinAskStream).pipe(
    ops.map(lambda ps: (float(ps[0]) + float(ps[1])) / 2))

priceSellLCStream = priceSellMainStream.pipe(
    ops.map(lambda p: p - ALPHA))

initialOrderStream = canOrderStream.pipe(
    ops.filter(bool))

buyMainOrderStream = rx.zip(initialOrderStream, priceBuyMainStream).pipe(
    ops.map(lambda res: buy(res[1])))

buyLCOrderStream = rx.zip(initialOrderStream, priceBuyLCStream).pipe(
    ops.map(lambda res: buy(res[1])))

sellMainOrderStream = rx.zip(initialOrderStream, priceSellMainStream).pipe(
    ops.map(lambda res: sell(res[1])))

sellLCOrderStream = rx.zip(initialOrderStream, priceSellLCStream).pipe(
    ops.map(lambda res: sell(res[1])))

# other

nowStream = rx.interval(0.01).pipe(
    ops.map(lambda _: str(datetime.now())),
)
