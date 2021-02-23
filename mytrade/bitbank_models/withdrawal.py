from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Withdrawal:
    uuid: str = None
    asset: str = None
    amount: int = None
    account_uuid: str = None
    fee: int = None
    status: str = None
    label: str = None
    txid: str = None
    address: str = None
    requested_at: int = None
