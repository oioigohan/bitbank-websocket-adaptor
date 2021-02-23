from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Trade:
    trade_id: int = None
    pair: str = None
    order_id: int = None
    side: str = None
    type: str = None
    amount: str = None
    price: str = None
    market_taker: str = None
    fee_amount_base: str = None
    fee_amount_quote: str = None
    executed_at: float = None


@dataclass_json
@dataclass
class TradesData:
    trades: List[Trade] = None
