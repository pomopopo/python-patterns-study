#!/usr/local/bin/python3
"""
*"惰性求值"侬做撒子?
让类的属性在需要的时候才求值.

*背景知识
- 惰性求值又称:惰性计算/懒惰求值, 也称为传需求调用(call-by-need). 目的是
最小化计算机的工作, 例如构造一个无限的数据类型.
- 惰性求值的相反方向是及早求值, 是大多数编程语言的计算方式.
- 惰性求值特别适用于函数式编程语言. 表达式绑定到变量后, 不离开求值, 只在取用
的时候求值.
- 和 python 中 iter, yield 的思想是类似的
- 生成器! 就是惰性求值的

*例子说明
某人, 有亲戚和父母, 调查关系的时候, 查值之前, 该属性对应的属性并没有加载, 只有
在调用后, 才有新属性写入到 __dict__ 字典.
                        +-----------------+
+-----------------+     |     Person      |
|lazy_property  #-----+ +-----------------+
+-----------------+   | |  __init__       |
|  __init__(func) |   | |                 |
|  __get__        |   | |  +-----------+  |
+-----------------+   +--->( relatives )  |
                        |  +-----------+  |
                        |                 |
+---------------------+ |  +-----------+  |
|lazy_property2(fn) #----->( parents   )  |
|    @property        | |  +-----------+  |
|    _lazy_property() | |                 |
+---------------------+ +-----------------+



*懒惰求值模式的使用场景?
- 构造无限的数据类型(例如一个Fib这种无限数列, 或者巨型的文件)
- 性能提升(内存使用和消耗的时间)

*参考
https://github.com/faif/python_patterns
https://en.wikipedia.org/wiki/Lazy_evaluation

*概述
只有在需要的时候, 才对表达式进行计算求值, 而且可以避免重复计算.
"""

import functools


class lazy_property:
    def __init__(self, function):
        self.function = function
        functools.update_wrapper(self, function)

    def __get__(self, obj, type_):
        if obj is None:
            return self
        val = self.function(obj)
        obj.__dict__[self.function.__name__] = val
        return val


def lazy_property2(fn):
    attr = f'_lazy__{fn.__name__}'

    @property
    def _lazy_property(self):
        if not hasattr(self, attr):
            setattr(self, attr, fn(self))
        return getattr(self, attr)

    return _lazy_property


class Person:
    def __init__(self, name, occupation) -> None:
        self.name = name
        self.occupation = occupation
        self.call_count = 0

    @lazy_property
    def relatives(self):
        # 收集亲戚信息,假定耗时比较多的那种
        relatives = 'Many relatives'
        return relatives

    @lazy_property2
    def parents(self):
        self.call_count += 1
        return 'Father and Monther'


def main():
    """
    >>> boy = Person('John', 'Coder')
    >>> boy.name, boy.occupation
    ('John', 'Coder')

    # 调用 relatives 前, 字典里是没有 relatives 的
    >>> sorted(boy.__dict__.items())
    [('call_count', 0), ('name', 'John'), ('occupation', 'Coder')]

    # 调用 relatives 这个被惰性求值修饰过
    >>> boy.relatives
    'Many relatives'

    # 查看字典, 多了 relatives的内容
    >>> sorted(boy.__dict__.items())
    [('call_count', 0), ..., ('relatives', 'Many relatives')]

    # 调用父母信息, 反馈信息, 且字典继续加内容
    >>> boy.parents
    'Father and Monther'

    >>> sorted(boy.__dict__.items())
    [('_lazy__parents', 'Father and Monther'), ('call_count', 1), ...]

    # 再次调用, 检查 call_count 是否变化
    >>> boy.parents
    'Father and Monther'

    # 再次调用 parents 后 call_count 不增加,
    # 即函数虽然返回了属性值, 但是并没有真的执行.
    >>> boy.call_count
    1
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
