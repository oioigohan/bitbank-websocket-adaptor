from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Account:
    uuid: str = None
    label: str = None
    address: str = None


@dataclass_json
@dataclass
class AccountsData:
    accounts: List[Account] = None
