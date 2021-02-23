from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Order:
    order_id: int = None
    pair: str = None
    side: str = None
    type: str = None
    start_amount: str = None
    remaining_amount: str = None
    executed_amount: str = None
    price: str = None
    average_price: str = None
    ordered_at: float = None
    canceled_at: int = None
    status: str = None


@dataclass_json
@dataclass
class OrdersData:
    orders: List[Order] = None


@dataclass_json
@dataclass
class OrderWithLosscut:
    main_order: Order = None
    losscut_order: Order = None


@dataclass_json
@dataclass
class TwinOrders:

    buy_orders: OrderWithLosscut = None
    sell_orders: OrderWithLosscut = None

    @property
    def ids(self) -> List[int]:
        return [
            self.buy_orders.main_order.order_id,
            self.buy_orders.losscut_order.order_id,
            self.sell_orders.main_order.order_id,
            self.sell_orders.losscut_order.order_id]

    def update(self, orders: OrdersData):

        ids = self.ids

        for order in orders:
            if order.order_id == ids[0]:
                self.buy_orders.main_order = order
            elif order.order_id == ids[1]:
                self.buy_orders.losscut_order = order
            elif order.order_id == ids[2]:
                self.sell_orders.main_order = order
            elif order.order_id == ids[3]:
                self.sell_orders.losscut_order = order

            assert order in ids
