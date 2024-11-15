# Warehouse Management
Консольная система управления складом.

## Системные требования
- `Python` версии `3.12` или выше (исключая версию `3.12.5`, на ней не работает `black`)
- `Poetry` версии `1.8.3` или выше

## Установка

1. Склонируйте репозиторий:
```
git clone ...
```

2. Перейдите в директорию с проектом:
```
cd ...
```

3. Установите зависимости:
```
poery install
```

## Проверка и тестирование

Для запуска инструментов форматирования или тестов используйте Makefile

- Запуск линтера
```
make lint
```

- Запуск форматирования
```
make format
```

- Запуск доменных тестов
```
make domain-test
```

- Запуск тестов инфраструктуры
```
make infra-test
```

## Запуск

Для запуска приложения выполните скрипт `main.py`:
```
python main.py
```

## Эксплуатация

На каждом эта предлагается выбрать операцию
```
1 - Add product
2 - Add order
3 - Add customer
4 - Get customers list
5 - Close application
Choose operation:
```

### Добавление продукта

Чтобы добавить продукт на склад, заполните название продукта, количество на складе и цену
```
Product name:myproducts
Product quantity:100
Product price:20
New product created: Product(id=None, name='myproducts', quantity=100, price=20)
```

### Добавление заказа

Чтобы добавить заказ, заполните id продуктов через запятую
```
Product ids (separate by comma):1,2
New order created: Order(id=None, products=[Product(id=1, name='test1', quantity=1, price=100.0), Product(id=2, name='test2', quantity=10, price=50.0)])
```

### Добавление покупателя

Чтобы добавить покупателя, заполните имя покупателя и id заказов через запятую
```
Order ids (separate by comma):2,3
New customer created: Customer(id=None, name='Sam', orders=[Order(id=2, products=[Product(id=2, name='test2', quantity=10, price=50.0), Product(id=1, name='test1', quantity=1, price=100.0)]), Order(id=3, products=[Product(id=1, name='test1', quantity=1, price=100.0), Product(id=2, name='test2', quantity=10, price=50.0)])])
```

### Список покупателей

Список покупателей ввыводится в формате "Имя покупателя >> Список заказов"
```
[Customer John Doe] >> ORDERS [[Order(id=1, products=[Product(id=1, name='test1', quantity=1, price=100.0), Product(id=2, name='test2', quantity=10, price=50.0)]), Order(id=2, products=[Product(id=2, name='test2', quantity=10, price=50.0), Product(id=1, name='test1', quantity=1, price=100.0)])]]
[Customer Sam] >> ORDERS [[Order(id=2, products=[Product(id=2, name='test2', quantity=10, price=50.0), Product(id=1, name='test1', quantity=1, price=100.0)]), Order(id=3, products=[Product(id=1, name='test1', quantity=1, price=100.0), Product(id=2, name='test2', quantity=10, price=50.0)])]]
```
