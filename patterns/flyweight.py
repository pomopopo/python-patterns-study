#!/usr/local/bin/python3
"""
*拔刀吧诸君
用与程序运行时减少对象的数量. 享元, 作为一个类, 可以被多个上下文共享.
与非共享的类有明显区别.

享元的状态不受其上下文影响, 而是作为本身状态存在. 享元之所以能被共享,
在于把该对象的状态从其上下文中分离(解耦)出来.

*犯罪现场回顾
建对象池, 存初始化好的对象. 当需要一个的时候, 先在池里查看有没有可用的,
不要上来就创建. 这样就可以减少程序初始化对象的数目.

*案卷
https://githut.com/faif/python_patterns

*案情分析
python 本身是用 GC 机制的--当一个实例的引用计数为0时, GC 就会回收内存.

有的时候(例如循环引用), GC 无法判断, 就不回收, 只能手动运行垃圾回收器(这
时候 del 变量名 并不起作用).

弱引用不会增加被引用对象的引用计数, 垃圾回收器也会当做没看到.

所以弱引用的一个用处就是实现缓存! 当引用对象存在时, 则对象可用. 当对象不
存在时, 返回 None, 程序不会因对象不存在而报错 -- 此乃有则用, 无则建的技术.

*同类作案手法
- python ecosystem 下用了
https://docs.python.org/3/library/sys.html#sys.intern

*概述
相似对象间共享数据, 可以减少内存使用.
"""


import weakref


class Card:
    '''享元'''

    # weakref.WeakValueDictionary([dict]) 创建value为弱引用对象的字典
    # 没有实例的时候, 就可以自动垃圾回收了
    _pool = weakref.WeakValueDictionary()

    def __new__(cls, value, suit):
        # 有则返回
        obj = cls._pool.get(value+suit)
        # 无则创建
        if obj is None:
            obj = object.__new__(Card)
            cls._pool[value+suit] = obj
            # 其实干了 __init__ 里的活
            obj.value, obj.suit = value, suit
        return obj

    # 如果这里放上
    # def __init__(...)
    #     obj.value, obj.suit = value, suit
    # 不用 __new__(...) 那就变成传统的普通类了

    def __repr__(self):
        return f'<Card: {self.value}{self.suit}>'


def main():
    """
    >>> c1 = Card('9', 'h')
    >>> c2 = Card('9', 'h')
    >>> c1, c2
    (<Card: 9h>, <Card: 9h>)

    >>> c1 == c2, c1 is c2
    (True, True)

    >>> c1.new_attr = 'temp'
    >>> c3 = Card('9', 'h')
    >>> if hasattr(c3, 'new_attr'):
    ...     print(c3.new_attr)
    temp

    >>> print(c3.__dict__)
    {'value': '9', 'suit': 'h', 'new_attr': 'temp'}

    >>> Card._pool.clear()
    >>> c4 = Card('9', 'h')
    >>> hasattr(c4, 'new_attr')
    False

    >>> c4.__dict__
    {'value': '9', 'suit': 'h'}

    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
