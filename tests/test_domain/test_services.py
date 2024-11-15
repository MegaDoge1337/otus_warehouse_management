import functools
import unittest
from unittest.mock import Mock

from domain.models import Customer, Order, Product
from domain.services import WarehouseService


def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                f(*new_args)

        return wrapper

    return decorator


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.product_repo = Mock()
        self.order_repo = Mock()
        self.customer_repo = Mock()

        self.service = WarehouseService(
            product_repo=self.product_repo,
            order_repo=self.order_repo,
            customer_repo=self.customer_repo,
        )

    @cases([("product", 10, 500.0)])
    def test_create_product(self, name, quantity, price):
        self.product_repo.add.return_value = None
        product = self.service.create_product(name, quantity, price)

        self.assertEqual(product.name, name)
        self.assertEqual(product.quantity, quantity)
        self.assertEqual(product.price, price)

    @cases(
        [
            (
                "John",
                [
                    Order(1, []),
                    Order(2, []),
                ],
            )
        ]
    )
    def test_create_customer(self, name, orders):
        self.customer_repo.add.return_value = None
        customer = self.service.create_customer(name, orders)

        self.assertEqual(customer.name, name)
        self.assertEqual(customer.orders[0].id, orders[0].id)
        self.assertEqual(customer.orders[1].id, orders[1].id)

    @cases(
        [
            (
                [
                    Product(1, "test1", 1, 1),
                    Product(2, "test2", 2, 2),
                ]
            )
        ]
    )
    def test_create_order(self, products):
        self.order_repo.add.return_value = None
        order = self.service.create_order(products)

        self.assertEqual(order.products[0].id, products[0].id)
        self.assertEqual(order.products[0].name, products[0].name)
        self.assertEqual(order.products[0].quantity, products[0].quantity)
        self.assertEqual(order.products[0].price, products[0].price)

        self.assertEqual(order.products[1].id, products[1].id)
        self.assertEqual(order.products[1].name, products[1].name)
        self.assertEqual(order.products[1].quantity, products[1].quantity)
        self.assertEqual(order.products[1].price, products[1].price)

    @cases(
        [
            (
                1,
                "John",
                [
                    Order(1, []),
                    Order(2, []),
                ],
            )
        ]
    )
    def test_get_customer_list(self, id, name, orders):
        self.customer_repo.list.return_value = [Customer(id, name, orders)]
        customers = self.service.get_customers_list()

        self.assertEqual(customers[0].id, id)
        self.assertEqual(customers[0].name, name)
        self.assertEqual(customers[0].orders[0].id, orders[0].id)
        self.assertEqual(customers[0].orders[1].id, orders[1].id)

    @cases(
        [
            (1, "test1", 1, 1),
        ]
    )
    def test_get_product(self, id, name, quantity, price):
        self.product_repo.get.return_value = Product(id, name, quantity, price)
        product = self.service.get_product(id)

        self.assertEqual(product.id, id)
        self.assertEqual(product.name, name)
        self.assertEqual(product.quantity, quantity)
        self.assertEqual(product.price, price)

    @cases(
        [
            (
                1,
                [
                    Product(1, "test1", 1, 1),
                    Product(2, "test2", 2, 2),
                ],
            )
        ]
    )
    def test_get_order(self, id, products):
        self.order_repo.get.return_value = Order(id, products)
        order = self.service.get_order(id)

        self.assertEqual(order.id, id)
        self.assertEqual(order.products[0].id, products[0].id)
        self.assertEqual(order.products[0].name, products[0].name)
        self.assertEqual(order.products[0].quantity, products[0].quantity)
        self.assertEqual(order.products[0].price, products[0].price)
        self.assertEqual(order.products[1].id, products[1].id)
        self.assertEqual(order.products[1].name, products[1].name)
        self.assertEqual(order.products[1].quantity, products[1].quantity)
        self.assertEqual(order.products[1].price, products[1].price)
