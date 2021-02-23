from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Pair:
    name: str = None
    base_asset: str = None
    maker_fee_rate_base: str = None
    taker_fee_rate_base: str = None
    maker_fee_rate_quote: str = None
    taker_fee_rate_quote: str = None
    unit_amount: str = None
    limit_max_amount: str = None
    market_max_amount: str = None
    market_allowance_rate: str = None
    price_digits: int = None
    amount_digits: int = None
    is_enabled: bool = None
    stop_order: bool = None
    stop_order_and_cancel: bool = None


@dataclass_json
@dataclass
class PairsData:
    pairs: List[Pair] = None
