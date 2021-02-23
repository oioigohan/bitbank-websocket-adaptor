from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Ohlcv:
    ohlcv: List[List] = None
    type: str = None


@dataclass_json
@dataclass
class CandleStickData:
    candlestick: List[Ohlcv] = None
    timestamp: str = None
