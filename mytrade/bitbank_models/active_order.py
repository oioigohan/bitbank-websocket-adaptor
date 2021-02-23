from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from rx.subject import Subject
from mytrade.bitbank_models import Order, OrdersData
from ..streams import buy, sell, buyLC, sellLC, cancelOrder
from ..parameters import PAIR, AMOUNT, ALPHA, BETA, GAMMA


class ActiveOrder(Order, Subject):

    def cancel(self, parameter_list):
        pass


class OrderWithLossCut(ActiveOrder):

    order: ActiveOrder = None
    orderLC: ActiveOrder = None

    def __init__(self, side: str, price: float, amount: float = AMOUNT):

        if side == 'buy':
            self.order = buy(price, amount)
            self.orderLC = buy(price + ALPHA, amount)

        elif side == 'sell':
            self.order = sell(price, amount)
            self.orderLC = sell(price - ALPHA, amount)
