#!/usr/local/bin/python3
"""
*是什么?
将一组对象, 视为同类的 **一个实例**.
做法是降类组织成树, 具备了部分--整体的继承关系.
客户端对待单独的类和合成的类, 是一致的.
关键点: 树枝里组合该接口, 内部含有list, 里边放component

*注意事项
有两种构成方式, 安全模式和透明模式.
- 安全模式下, 最下级的对象没有 add/remove 功能, 中间的树枝构件可以管理下级对象(add/remove)
    优点: 安全, 不会调用到不存在的接口
    缺点: 不够透明, 树叶类和合成类具有不同的接口, 调用方法时要区别是树枝还是树叶
- 透明模式下, 所有构件, 无论树枝还是树叶, 都要具备 add/remove, 但是树叶中相应方法不做任何操作.
    优点: 接口一致, 操作一致, 没有接口层次上的区别
    缺点: 不安全, 调用树叶的 add/remove 容易run time error
一般推荐透明性的实现方式

*本例做了什么?
本例实现了一个图形类, 既可以是个椭圆(或者方块), 也可以是几个图形的合成,
每个图形都可以打印.

graphic=CompositeGraphic()
graphic.render()
            |           +-------+--------+
            |           |CompositeGraphic|
            |           +----------------+
            +---------->+ + add()        |
                        | + remove()     |
                +------>+ + render()     +<------+
                |       +----------------+       |
                |                                |
        +-------+--------+                +------+---------+
        |CompositeGraphic| gr1            |CompositeGraphic| gr2
        +----------------+                +----------------+
        | + add()        |                | + add()        |
        | + remove()     |                | + remove()     |
        | + render()     |                | + render()     |
        +-+---------+----+                +--+-----------+-+
          ^         ^                        ^           ^
- - - - - + - - - - + - - Graphic  <ABC> - - + - - - - - + - - - - -
          |         |                        |           |
+---------+-+     +-+---------+     +--------+--+     +--+-------+
|  Ellipse  | e1  |  Ellipse  | e2  |  Ellipse  | e3  |   Cube   | c1
+-----------+     +-----------+     +-----------+     +----------+
|+ render() |     |+ render() |     |+ render() |     |+ render()|
+-----------+     +-----------+     +-----------+     +----------+

*优缺点
- 优点: 所有类有相同的接口, 在客户端看来, 没有了 树叶类与树枝类接口层次的区别
- 缺点: 不安全. 树叶也有

*s使用场景
部分--整体场景: 如树形菜单, 目录树(文件系统), 文件/文件夹的管理

*参考
https://github.com/faif/python_patterns
https://www.cnblogs.com/qlqwjy/p/11049493.html
https://www.cnblogs.com/houss/p/11206945.html

*概述
如何把一组对象视为一个实例.
"""


from abc import ABC, abstractmethod


class Graphic(ABC):
    @abstractmethod
    def render(self):
        raise NotImplementedError('u need to impl this.')


class CompositeGraphic(Graphic):
    def __init__(self) -> None:
        self.graphics = []

    def render(self):
        for graph in self.graphics:
            graph.render()

    def add(self, graphic):
        self.graphics.append(graphic)

    def remove(self, graphic):
        self.graphics.remove(graphic)


class Ellipse(Graphic):
    def __init__(self, name):
        self.name = name

    def render(self):
        print(f'Ellipse: {self.name}')


class Cube(Graphic):
    def __init__(self, name):
        self.name = name

    def render(self):
        print(f'Cube: {self.name}')


def test():
    e_1 = Ellipse('E1')
    e_2 = Ellipse('E2')
    e_3 = Ellipse('E3')
    c_1 = Cube('C1')

    gr1 = CompositeGraphic()
    gr2 = CompositeGraphic()

    gr1.add(e_1)
    gr1.add(e_2)
    gr1.render()

    print('-'*4)
    gr2.add(e_3)
    gr2.add(c_1)
    gr2.render()

    print('-'*4)
    graphic = CompositeGraphic()
    graphic.add(gr1)
    graphic.add(gr2)
    graphic.render()


def main():
    """
    >>> e_1 = Ellipse('E1')
    >>> e_2 = Ellipse('E2')
    >>> e_3 = Ellipse('E3')
    >>> c_1 = Cube('C1')

    # 第一个合成类
    >>> gr1 = CompositeGraphic()
    >>> gr1.add(e_1)
    >>> gr1.add(e_2)
    >>> gr1.render()
    Ellipse: E1
    Ellipse: E2

    # 第二个合成类
    >>> gr2 = CompositeGraphic()
    >>> gr2.add(e_3)
    >>> gr2.add(c_1)
    >>> gr2.render()
    Ellipse: E3
    Cube: C1

    # 多个合成类可以再合成, 只要都有 render 就好
    # 结果就跟一个类的操作一样一样的
    >>> graphic = CompositeGraphic()
    >>> graphic.add(gr1)
    >>> graphic.add(gr2)
    >>> graphic.render()
    Ellipse: E1
    Ellipse: E2
    Ellipse: E3
    Cube: C1
    """


if __name__ == "__main__":
    test()

    import doctest
    doctest.testmod(verbose=True)
