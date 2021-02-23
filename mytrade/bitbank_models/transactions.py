from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Transaction:
    amount: str = None
    executed_at: int = None
    price: str = None
    side: str = None
    transaction_id: int = None


@dataclass_json
@dataclass
class TransactionsData:
    transactions: List[Transaction] = None
