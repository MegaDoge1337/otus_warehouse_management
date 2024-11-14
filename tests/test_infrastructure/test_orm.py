import unittest
import functools

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.orm import Base, ProductORM, OrderORM, CustomerORM

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
      self.database_url = "sqlite:///:memory:"
      self.engine = create_engine(self.database_url)

      SessionFactory=sessionmaker(bind=self.engine)
      Base.metadata.create_all(self.engine)

      self.session = SessionFactory()
    
    @cases([("product", 10, 500.0)])
    def test_add_get_product(self, name, quantity, price):
      product_orm = ProductORM(
          name=name,
          quantity=quantity,
          price=price
      )

      self.session.add(product_orm)
      self.session.commit()

      product_orm = self.session.query(ProductORM).one()
      
      self.assertEqual(product_orm.name, name)
      self.assertEqual(product_orm.price, price)
      self.assertEqual(product_orm.quantity, quantity)

      self.session.query(ProductORM).filter_by(id=product_orm.id).delete()
      self.session.commit()
    
    @cases([([])])
    def test_add_get_order(self, products):
      order_orm = OrderORM(products=products)

      self.session.add(order_orm)
      self.session.commit()

      order_orm = self.session.query(OrderORM).one()
      
      self.assertEqual(len(order_orm.products), len(products))
      self.assertTrue(isinstance(order_orm.products, list))

      self.session.query(OrderORM).filter_by(id=order_orm.id).delete()
      self.session.commit()

    @cases([("John", [])])
    def test_add_get_customer(self, name, orders):
      customer_orm = CustomerORM(name=name,
                                 orders=orders)

      self.session.add(customer_orm)
      self.session.commit()

      customer_orm = self.session.query(CustomerORM).one()
      
      self.assertEqual(customer_orm.name, name)
      self.assertEqual(len(customer_orm.orders), len(orders))
      self.assertTrue(isinstance(customer_orm.orders, list))

      self.session.query(CustomerORM).filter_by(id=customer_orm.id).delete()
      self.session.commit()
    
    @cases([("product", 10, 500.0)])
    def test_order_product_relations(self, product_name, product_quantity, product_price):
      product_orm = ProductORM(
          name=product_name,
          quantity=product_quantity,
          price=product_price
      )

      self.session.add(product_orm)
      self.session.commit()

      product_orm = self.session.query(ProductORM).one()

      order_orm = OrderORM(products=[product_orm])

      self.session.add(order_orm)
      self.session.commit()

      order_orm = self.session.query(OrderORM).one()

      self.assertEqual(order_orm.products[0].id, product_orm.id)
      self.assertEqual(order_orm.products[0].name, product_orm.name)
      self.assertEqual(order_orm.products[0].quantity, product_orm.quantity)
      self.assertEqual(order_orm.products[0].price, product_orm.price)

      self.session.query(ProductORM).filter_by(id=product_orm.id).delete()
      self.session.query(OrderORM).filter_by(id=order_orm.id).delete()
      self.session.commit()


    @cases([("John", [])])
    def test_customer_order_relations(self, customer_name, order_products):
      order_orm = OrderORM(products=order_products)

      self.session.add(order_orm)
      self.session.commit()

      order_orm = self.session.query(OrderORM).one()

      customer_orm = CustomerORM(name=customer_name,
                                 orders=[order_orm])
      
      self.session.add(customer_orm)
      self.session.commit()

      customer_orm = self.session.query(CustomerORM).one()

      self.assertEqual(customer_orm.orders[0].id, order_orm.id)

      self.session.query(OrderORM).filter_by(id=order_orm.id).delete()
      self.session.query(CustomerORM).filter_by(id=customer_orm.id).delete()
      self.session.commit()
