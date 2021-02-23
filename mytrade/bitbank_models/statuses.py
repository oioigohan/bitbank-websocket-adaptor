from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Status:
    pair: str = None
    status: str = None
    min_amount: str = None


@dataclass_json
@dataclass
class StatusesData:
    statuses: List[Status] = None
