#!/usr/local/bin/python3
"""
*啥?!
定义一族算法, 封装, 并保持内部互不交互.
策略模式可以让客户端用算法的时候, 独立变化(而不用改类)

- 对 python 而言, 不需要再去定义个类(没必要), 直接用高阶函数, 就可以把函数注入到类中.

*本例
一个订单类, 引入了2个打折算法(函数).

+--------------------+ strategy        +----------------------+
| Context            +<>-------------->+ Strategy             | virtual
+--------------------+                 +----------------------+
| ContextInterface() |                 | AlgorithmInterface() |
+--------------------+                 +--------^-------------+
                                                |
            +-----------------------+-----------+------------+
            |                       |                        |
+-----------+---------+ +-----------+----------+ +-----------+----------+
| ConcreteStrategyA   | | ConcreteStrategyB    | | ConcreteStrategyC    |
+---------------------+ +----------------------+ +----------------------+
|AlgorithmInterface() | | AlgorithmInterface() | | AlgorithmInterface() |
+---------------------+ +----------------------+ +----------------------+

*用途
- 销售的折扣算法
- 算法使用了客户不应该知道的数据, 避免暴露复杂的/与算法相关的数据结构.
- 要用一个算法的不同变体, 如不同的时间/空间的权衡.

*概述
可以运行时选择算法.
"""

# 例子1: 订单


class Order:
    def __init__(self, price, discount_strategy=None):
        self.price = price
        self.discount_strategy = discount_strategy

    def price_after_discount(self):
        discount = self.discount_strategy(
            self) if self.discount_strategy else 0
        return self.price - discount

    def __repr__(self):
        return f'<Price: {self.price:0.2f}, price after discount: {self.price_after_discount():0.2f}>'


def ten_percent_discount(order):
    return order.price*0.1


def on_sale_discount(order):
    discount = order.price*0.25+20
    if discount > order.price:
        # 注意这里, 折扣超过原价的话, 就不能折了, 否则在调用处会变成负数
        return 0
    else:
        return discount


def test_example_1():
    """
    >>> print(Order(27))
    <Price: 27.00, price after discount: 27.00>

    >>> print(Order(27,discount_strategy=ten_percent_discount))
    <Price: 27.00, price after discount: 24.30>

    >>> print(Order(27,discount_strategy=on_sale_discount))
    <Price: 27.00, price after discount: 0.25>

    >>> print(Order(26,discount_strategy=on_sale_discount))
    <Price: 26.00, price after discount: 26.00>
    """


# 例子2: 更虚拟一些

import types


class Strategy2:
    def __init__(self, func=None):
        self.name = 'Stragery2 Example 0'
        # print(func)
        if func:
            # 注意这里 types 用法!
            self.execute = types.MethodType(func, self)

    def execute(self):
        print(self.name)


def exec_replacement_1(self):
    print(f'{self.name} from exec 1')


def exec_replacement_2(self):
    print(f'{self.name} from exec 2')


def test_example_2():
    """
    >>> s0 = Strategy2()
    >>> s0.execute()
    Stragery2 Example 0

    >>> s1 = Strategy2(exec_replacement_1)
    >>> s1.name = 'Strategy Example 1'
    >>> s1.execute()
    Strategy Example 1 from exec 1

    >>> s2 = Strategy2(exec_replacement_2)
    >>> s2.name = 'Strategy_2'
    >>> s2.execute()
    Strategy_2 from exec 2

    """

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

