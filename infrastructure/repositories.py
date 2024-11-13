from sqlalchemy.orm import Session
from typing import List
from domain.models import Order, Product, Customer
from domain.repositories import ProductRepository, OrderRepository, CustomerRepository
from .orm import ProductORM, OrderORM, CustomerORM

class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session=session

    def add(self, product:Product):
        product_orm = ProductORM(
            name=product.name,
            quantity=product.quantity,
            price=product.price
        )
        self.session.add(product_orm)

    def get(self, product_id: int)->Product:
        product_orm= self.session.query(ProductORM).filter_by(id=product_id).one()
        return Product(id=product_orm.id, name=product_orm.name, quantity=product_orm.quantity, price=product_orm.price)

    def list(self) -> List[Product]:
        products_orm= self.session.query(ProductORM).all()
        return [Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price) for p in products_orm]

class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session=session

    def add(self, order:Order):
        order_orm = OrderORM()
        order_orm.products = [self.session.query(ProductORM).filter_by(id=p.id).one() for p in order.products]
        self.session.add(order_orm)

    def get(self, order_id: int)->Order:
        order_orm= self.session.query(OrderORM).filter_by(id=order_id).one()
        products = [Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price) for p in order_orm.products]
        return Order(id=order_orm.id, products=products)

    def list(self) -> List[Product]:
        orders_orm= self.session.query(OrderORM).all()
        orders=[]
        for order_orm in orders_orm:
            products = [Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price) for p in order_orm.products]
            orders.append(Order(id=order_orm.id, products=products))
        return orders

class SqlAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, session: Session):
        self.session=session

    def add(self, customer: Customer):
        customers_orm = CustomerORM()
        customers_orm.name = customer.name
        customers_orm.orders = [self.session.query(OrderORM).filter_by(id=o.id).one() for o in customer.orders]
        self.session.add(customers_orm)

    def get(self, customer_id: int) -> Customer:
        customers_orm = self.session.query(CustomerORM).filter_by(id=customer_id).one()
        orders = [
            Order(id=o.id, products=[
                Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price) 
                for p in o.products
            ]) 
            for o in customers_orm.orders
        ]
        return Customer(id=customers_orm.id, name=customers_orm.name, orders=orders)

    def list(self) -> List[Customer]:
        customers_orm = self.session.query(CustomerORM).all()
        customers = []
        for customer_orm in customers_orm:
            orders = [
                Order(id=o.id, products=[
                    Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price) 
                    for p in o.products
                ]) 
                for o in customer_orm.orders
            ]
            customers.append(Customer(id=customer_orm.id, name=customer_orm.name, orders=orders))
        return customers




