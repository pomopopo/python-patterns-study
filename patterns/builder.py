#!/usr/local/bin/python3
"""
*汝欲何为?
分离复杂对象的创建和展示部分, 同样的创建过程可以被同家族复用.
当必须分离一个对象参数和真正的呈现时(通常用于抽象), 很有用.


*本例做撒子?
例一, 用了抽象基类, 当需要初始化(__init__)时, 指定所需具体步骤, 实例子类去完成
这些具体步骤.

例一的结构:
            +-----------------+
            |  <<interface>>  |
            | Builder         |
            | Building        |
            +-----------------+
            | +build_floor()  |
            | +buid_size()    |
            | +__repr__()     |
            +--+-----------+--+
               ^           ^
               |           |
+--------------+--+     +--+--------------+
| ConcreteBuilder |     | ConcreteBuilder |
| House           |     | Flat            |
+-----------------+     +-----------------+
| +build_floor()  |     | +build_floor()  |
| +build_size()   |     | +build_size()   |
| +__repr__()     |     | +__repr__()     |
+-----------------+     +-----------------+


有的语言(如c++)有时候需要更复杂的实现方式----创建时不支持多态. 这时候要通过外部
不同的类来实现.
然, python 无需如此. 例二演示了...?

对,这才是通常的 Builder 模式:
        +-------------+     +---------------+
        |    user     +<>-->+    Builder    |
        +-------------+     +---------------+
        |construct(). |     | +build_part() |
        +-----------|-+     +-------+-------+
                    |               ^
+-------------------+---+           |
|for item in structure: |   +-------+-------+   +-------+
|  builder.build_part() |   |ConcreteBuilder+<--+Product|
+-----------------------+   +---------------+   +-------+
                            | +build_part() |
                            | +get_result() |
                            +---------------+

*何处可用?
- 相同方法,不同执行顺序, 产生不同的结果时
- 多个零部件, 都可以装配到一个对象中, 但是产生不同的结果时
- 产品类非常复杂, 或者产品类中调用顺序不同会产生不同结果----非常推荐使用
- 初始化对象特别复杂时(e.g. 参数多, 还有默认值)

*参考
https://githut.com/faif/python_patterns
https://blog.csdn.net/Burgess_zheng/article/details/86762248

*概述
解耦复杂对象的创建及其表示.
"""


# 例一, 抽象创建者: 抽象的楼
class Building:
    def __init__(self):
        self.build_floor()
        self.build_size()

    def build_floor(self):
        raise NotImplementedError

    def build_size(self):
        raise NotImplementedError

    def __repr__(self):
        """这个 floor 和 size 需要由具体类给出"""
        return f'Floor: {self.floor} | Size: {self.size}'


# 具体建筑物: 具体化
class House(Building):
    def build_floor(self):
        self.floor = 'One'

    def build_size(self):
        self.size = 'Big'


class Flat(Building):
    def build_floor(self):
        self.floor = 'Multi-floors'

    def build_size(self):
        self.size = 'Small'


# 例二, 很复杂的话, 将建造逻辑分离到新的函数, 或者新的类里的方法,都是极好的. 远比
# 扔在 __init__ 要好. (然, 其具体类无构造函数, 怪乎哉)


class ComplexBuilding:
    def __repr__(self) -> str:
        return f'Floor: {self.floor} | Size: {self.size}'


class ComplexHouse(ComplexBuilding):
    def build_floor(self):
        self.floor = 'One'

    def build_size(self):
        # 这里有点不一样 最后看结果
        self.size = 'Big n fancy'


def construct_building(cls):
    # 复杂情况就在类外面组装了
    my_building = cls()
    my_building.build_floor()
    my_building.build_size()
    return my_building


def main():
    """
    # 例一, 抽象类--具体类
    >>> house = House()
    >>> house
    Floor: One | Size: Big

    >>> flat = Flat()
    >>> flat
    Floor: Multi-floors | Size: Small

    # 例二, 组装函数放移到外面!
    >>> cplx_house = construct_building(ComplexHouse)
    >>> cplx_house
    Floor: One | Size: Big n fancy
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()
