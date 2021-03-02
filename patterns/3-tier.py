#!/usr/local/bin/python3
"""
*三层模式
按照 数据/业务逻辑/表示 三者互相分离组织应用程序的方式.

*tier vs layer
tier 是物理层, layer 是逻辑层.
3-tier 的 表现层, 逻辑层, 数据层 都是可以单独部署的, 算物理层.
一个应用中的 Controller, Service, Model 是逻辑划分的, 不能独立部署, 是逻辑层.

*分层架构是啥?
- 按照层次组织应用, 每层有自己特定的责任
- 每层为上层提供服务, 使用下层提供的服务
- 下面不看上面, 上面一般也不跨层调用下面

*本例干了啥?
本例实现了一个 数据/业务逻辑/表示 的三层模型, 表示层向业务逻辑层要数据, 逻辑层从
数据层读数据. 读的数据展示出来.

+---------------------+
|         Ui          |  tier-3 present
+---------------------+
| + get_product_list()|
| + get_product_info()|
+-----------+---------+
            ^
            |
+-----------+---------+
|    BusinessLogic    |  tier-2 business logic
+---------------------+
| + product_list()    |
| + product_info()    |
+-----------+---------+
            ^
            |
+-----------+---------+
|        Data         |  tier-1 data
+---------------------+
| milk   $1.5, 30     |
| eggs   $0.2, 100    |
| cheese $2.0, 10     |
+---------------------+

*优缺点
- 优点: 高内聚, 低耦合, 每层能独立进化, 伸缩性好, 复用/移植都很好
- 缺点: 一个请求要多个层处理, 层间通信影响性能

*概要
分离表示/应用处理/数据管理功能
"""


class Data:
    """数据层: 数据仓库"""
    products = {
        'milk': {'price': 1.5, 'qty': 30},
        'eggs': {'price': 0.2, 'qty': 100},
        'cheese': {'price': 2.0, 'qty': 10},
    }

    def __get__(self, obj, kls):
        # 这个 print 没啥大用, 但是 get 提供接口, 有大用
        print('(Fetching from Data Store)')
        return {'products': self.products}


class BusinessLogic:
    """业务逻辑层: 操作数据仓库实例的"""
    # 调用数据层, 就这么一处耦合
    data = Data()

    def product_list(self):
        return self.data['products'].keys()

    def product_info(self, product):
        return self.data['products'].get(product, None)


class Ui:
    """表示层: 展示的接口"""

    def __init__(self):
        # 调用逻辑层, 只在这一处耦合
        self.business_logic = BusinessLogic()

    def get_product_list(self):
        print('PRODUCT LIST:')
        for p in self.business_logic.product_list():
            print(p)
        print()

    def get_product_info(self, product):
        p_info = self.business_logic.product_info(product)
        if p_info:
            print('PRODUCT INFO:')
            print(
                f'Name: {product.title()}, '
                f'Price: {p_info.get("price",0):.2f}, '
                f'Qty: {p_info.get("qty",0):}'
            )
        else:
            print(
                f'Product "{product.title()}" does not exist in the records.')


def test():
    ui = Ui()
    ui.get_product_list()
    ui.get_product_info('cheese')
    ui.get_product_info('eggs')
    ui.get_product_info('milk')
    ui.get_product_info('bacon') # 失败的例子


def main():
    """
    >>> ui = Ui()
    >>> ui.get_product_list()
    PRODUCT LIST:
    (Fetching from Data Store)
    milk
    eggs
    cheese
    <BLANKLINE>

    >>> ui.get_product_info('cheese')
    (Fetching from Data Store)
    PRODUCT INFO:
    Name: Cheese, Price: 2.00, Qty: 10

    >>> ui.get_product_info('eggs')
    (Fetching from Data Store)
    PRODUCT INFO:
    Name: Eggs, Price: 0.20, Qty: 100

    >>> ui.get_product_info('milk')
    (Fetching from Data Store)
    PRODUCT INFO:
    Name: Milk, Price: 1.50, Qty: 30

    # 获取不到的例子
    >>> ui.get_product_info('bacon')
    (Fetching from Data Store)
    Product "Bacon" does not exist in the records.
    """


if __name__ == "__main__":
    # test()

    import doctest
    doctest.testmod(verbose=True)
