#!/usr/local/bin/python3
"""
*要点
__getattr__
getattr()
callable()

*概述
允许对象通过组合, 实现继承相同的代码重用.
"""


class Delegate:
    """被委托的类"""

    def __init__(self):
        self.p1 = 123

    def do_something(self, something):
        return f'Doing {something}'


class Delegator:
    """委托者, 实现对被委托者的访问封装"""

    def __init__(self, delegate):
        self.delegate = delegate

    def __getattr__(self, name):
        """这里是核心! 不是函数的返回属性, 是函数的去调用"""
        attr = getattr(self.delegate, name)

        if not callable(attr):
            return attr

        def wrapper(*args, **kwargs):
            return attr(*args, **kwargs)

        return wrapper


def main():
    """
    >>> dele = Delegator(Delegate())

    # 调用 Delegate 类的内容
    >>> dele.p1
    123

    >>> dele.p2
    Traceback (most recent call last):
    ...
    AttributeError: 'Delegate' object has no attribute 'p2'


    # 调用 Delegate 类的函数
    >>> dele.do_something('nothing')
    'Doing nothing'

    >>> dele.do_anything()
    Traceback (most recent call last):
    ...
    AttributeError: 'Delegate' object has no attribute 'do_anything'

    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
