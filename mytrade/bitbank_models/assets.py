from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Asset:
    asset: str = None
    free_amount: str = None  # 証拠金の残額
    amount_precision: int = None
    onhand_amount: str = None  # 合計の金額
    locked_amount: str = None  # 使用中の金額
    withdrawal_fee: str = None
    stop_deposit: bool = None
    stop_withdrawal: bool = None


@dataclass_json
@dataclass
class AssetsData:
    assets: List[Asset] = None
