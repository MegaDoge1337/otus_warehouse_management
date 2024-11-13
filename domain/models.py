from dataclasses import dataclass, field
from typing import List

@dataclass
class Product:
    id: int
    name:str
    quantity:int
    price:float

@dataclass
class Order:
    id: int
    products: List[Product] = field(default_factory=list)

    def add_product(self, product: Product):
        self.products.append(product)

@dataclass
class Customer:
    id: int
    name: str
    orders: List[Order] = field(default_factory=list)

    def add_order(self, order: Order):
        self.orders.append(order)
