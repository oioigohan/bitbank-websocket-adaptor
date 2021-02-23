import rx
from rx.operators import map, start_with
from .streams import *


myTradeStream = rx.combine_latest(
    rx.interval(0.01).pipe(
    map(lambda _: datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
),
    PriceLastBuyStream.pipe(map(lambda res: 'last buy: ' + str(res)), start_with('waiting...')),
    PriceLastSellStream.pipe(map(lambda res: 'last sell: ' + str(res)), start_with('waiting...')),
    PriceMinAskStream.pipe(map(lambda res: 'min ask: ' + str(res)), start_with('waiting...')),
    PriceMaxBidStream.pipe(map(lambda res: 'max bid: ' + str(res)), start_with('waiting...')),
)
