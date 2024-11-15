from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.services import WarehouseService
from infrastructure.database import DATABASE_URL
from infrastructure.orm import Base
from infrastructure.repositories import (
    SqlAlchemyCustomerRepository,
    SqlAlchemyOrderRepository,
    SqlAlchemyProductRepository,
)
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def main():
    session = SessionFactory()
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session)
    customer_repo = SqlAlchemyCustomerRepository(session)

    uow = SqlAlchemyUnitOfWork(session)

    warehouse_service = WarehouseService(product_repo, order_repo, customer_repo)

    with uow:
        while True:
            print("1 - Add product")
            print("2 - Add order")
            print("3 - Add customer")
            print("4 - Get customers list")
            print("5 - Close application")
            user_input = input("Choose operation:")

            if user_input == "1":
                product_name = input("Product name:")
                product_quantity = int(input("Product quantity:"))
                product_price = int(input("Product price:"))

                new_product = warehouse_service.create_product(
                    name=product_name, quantity=product_quantity, price=product_price
                )
                uow.commit()
                print(f"New product created: {new_product}")
                continue

            if user_input == "2":
                product_ids = input("Product ids (separate by comma):")
                products = []
                for product_id in product_ids.split(","):
                    products.append(
                        warehouse_service.get_product(product_id=int(product_id))
                    )

                new_order = warehouse_service.create_order(products=products)
                uow.commit()
                print(f"New order created: {new_order}")
                continue

            if user_input == "3":
                customer_name = input("Customer name:")
                order_ids = input("Order ids (separate by comma):")
                orders = []
                for order_id in order_ids.split(","):
                    orders.append(warehouse_service.get_order(order_id=int(order_id)))

                new_customer = warehouse_service.create_customer(
                    name=customer_name, orders=orders
                )
                uow.commit()
                print(f"New customer created: {new_customer}")
                continue

            if user_input == "4":
                for customer in warehouse_service.get_customers_list():
                    print(f"[Customer {customer.name}] >> ORDERS [{customer.orders}]")
                continue

            if user_input == "5":
                break


if __name__ == "__main__":
    main()
