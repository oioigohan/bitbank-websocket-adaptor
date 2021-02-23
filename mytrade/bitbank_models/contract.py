from typing import List, Union
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from mytrade.bitbank_models import Order, OrdersData, TwinOrders, \
    OrderWithLosscut, ContractType


@dataclass_json
@dataclass
class Contract:
    type: ContractType = None
    orders: Union[TwinOrders, OrderWithLosscut] = None
