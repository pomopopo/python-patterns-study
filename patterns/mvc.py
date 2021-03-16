#!/usr/local/bin/python3
"""
*是什么
通常 mvc 只视为一种模式, 而不被视为设计模式, 传统设计模式里不包含这个.
- m, Model 模型, 用于承载数据, 并对用户提交的请求进行处理. 分2类:
    - 数据承载 -- 数据模型
    - 业务处理 -- 业务模型
- v, View 视图, 为用户提供使用界面, 与用户直接交互.
- c, Controller 控制器, 接收请求, 并将请求跳转(转发重定向)到对应的 Model
进行处理, 处理结果返给控制器, 渲染后, 控制器返回结果给视图的请求处.

调用过程:
    1请求          +------------+  2调用模型
    +------------->+Controller-C+------------+
    |              |逻辑控制     |            |
    |              +-+--------+-+            |
    |                |        ^              v
+---+-----+          |        |        +-----+-----+
|View-V   |          |        |        |Model-M    |
|前端显示  +<---------+        +--------+服务、数据库  |
+---------+   4响应           3返回结果  +-----------+

*与三层架构的区别/联系:
- 三层架构: 表现 / 业务逻辑 / 数据访问 这三层.
- MVC: 三层架构的表现层, 用 MVC 模式展现, 实现业务与展示分离.

+---+-----+------------+
|   |     | View       |
|   | UI  | Controller |
| 3 |     | Model      |
|   +-----+------------+
| T |                  |
| i | Business Logic   |
| e |                  |
| r +------------------+
|   |                  |
|   | Data             |
|   |                  |
+---+------------------+



*概要
在 GUI 界面中, 分离数据及其表示.
"""


from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def get(self, item):
        pass

    @property
    @abstractmethod
    def item_type(self):
        pass


class ProductModel(Model):
    class Price(float):
        def __str__(self):
            return f'{self:.2f}'

    products = {
        'milk': {'price': Price(1.5), 'qty': 10},
        'eggs': {'price': Price(0.2), 'qty': 100},
        'cheese': {'price': Price(2), 'qty': 20},
    }

    item_type = 'product'

    def __iter__(self):
        yield from self.products

    def get(self, product):
        try:
            return self.products[product]
        except KeyError as e:
            raise KeyError(str(e) + 'not in model items list.')


class View(ABC):
    @abstractmethod
    def show_item_list(self, item_type, item_list):
        pass

    @abstractmethod
    def show_item_info(self, item_type, item_name, item_info):
        pass

    @abstractmethod
    def item_not_found(self, item_type, item_name):
        pass


class ConsoleView(View):
    def show_item_list(self, item_type, item_list):
        print(f'{item_type.upper()} LIST:')
        for item in item_list:
            print(item)
        print()

    @staticmethod
    def capitalizer(string):
        return string[0].upper() + string[1:].lower()

    def show_item_info(self, item_type, item_name, item_info):
        print(f'{item_type.upper()} INFO:')
        printout = f'Name: {item_name}'
        for k, v in item_info.items():
            printout += f', {self.capitalizer(str(k))}: {str(v)}'
        printout += '\n'
        print(printout)

    def item_not_found(self, item_type, item_name):
        print(item_type, item_name, 'does not exists in the records.')


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self):
        items = list(self.model)
        item_type = self.model.item_type
        self.view.show_item_list(item_type, items)

    def show_item_info(self, item_name):
        try:
            item_info = self.model.get(item_name)
        except:
            item_type = self.model.item_type
            self.view.item_not_found(item_type, item_name)
        else:
            item_type = self.model.item_type
            self.view.show_item_info(item_type, item_name, item_info)


def main():
    """
    >>> model = ProductModel()
    >>> view = ConsoleView()
    >>> controller = Controller(model, view)
    >>> controller.show_items()
    PRODUCT LIST:
    milk
    eggs
    cheese
    <BLANKLINE>

    >>> controller.show_item_info('cheese')
    PRODUCT INFO:
    Name: cheese, Price: 2.00, Qty: 20
    <BLANKLINE>

    >>> controller.show_item_info('eggs')
    PRODUCT INFO:
    Name: eggs, Price: 0.20, Qty: 100
    <BLANKLINE>

    >>> controller.show_item_info('milk')
    PRODUCT INFO:
    Name: milk, Price: 1.50, Qty: 10
    <BLANKLINE>

    >>> controller.show_item_info('kindle')
    product kindle does not exists in the records.

"""

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
