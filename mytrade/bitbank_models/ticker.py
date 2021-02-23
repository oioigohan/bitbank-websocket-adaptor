from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Ticker:
    sell: str = None
    buy: str = None
    high: str = None
    low: str = None
    last: str = None
    vol: str = None
    timestamp: float = None
