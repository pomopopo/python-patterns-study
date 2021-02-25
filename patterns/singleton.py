#!/usr/local/bin/python3
"""
*单例模式的用途?
单例模式的类只有一个实例.

*本例做了什么?
实现5种单例
- import 单例: 所有变量都绑定到模块. 模块只初始化一次. 线程安全!
- 函数装饰器单例. 利用函数闭包
- 类装饰器单例(__init__)
- 使用__new__ 实现单例, 不是真实的单例模式
- metaclass 单例

*常见使用场景?
- 替代全局变量

*要点
如果实例不错在, 就创建一个新的; 如果实例存在, 就返回已创建的实例.
*参考

*概述 TL;DR

"""

"""用 import 实现单例
背景知识: python 中, import 进来的模块, 是全局变量. 而且 id() 不变.

```
import abc as a   # 用系统模块演示, 不再创建新的了
import abc as b
id(a) == id(b)    # 导入的模块 id 相同

a.my_prop = 1     # 添加属性(简化,没用 hasattr 检查)
b.my_prop         # a 的属性 b自然是有的, 前面只是 as 么

```
"""

# """用函数闭包实现单例"""
def singleton_1_func_wrap(cls):
    _instances = {}

    def wrapper(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return wrapper


@singleton_1_func_wrap
class Worker_1:
    def __init__(self, a):
        print(a)


# """用类装饰器实现单例"""
class Singleton_2_class_wrap:
    def __init__(self, cls):
        self._cls = cls
        self._instances = {}

    def __call__(self, *args, **kwds):
        if self._cls not in self._instances:
            self._instances[self._cls] = self._cls(*args, **kwds)
        return self._instances[self._cls]


@Singleton_2_class_wrap
class Worker_2:
    def __init__(self, a):
        print(a)


# 用 __new__ 实现单例
class Singleton_3_new(object):
    """new的不是真单例,每次都还会执行__init__,并且后面结果会覆盖前面的!"""
    _instance = None

    def __new__(cls, *args, **kwargs) :
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        """这个init每次也还是会被执行"""
        self._a = args
        self._kw = kwargs
        print(self._a, self._kw)

# meatclass方式
class Singleton_4_meta(type):
    """核心是 type"""
    _instances = []

    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton_4_meta, cls).__call__(*args, **kwds)
        return cls._instances[cls]


class Worker_4(Singleton_4_meta):
    def __init__(self, *args, **kw):
        print(args, kw)

def main():
    """
    # 1. 用 import 实现单例
    >>> import abc as a   # 用系统模块演示, 不再创建新的了
    >>> import abc as b
    >>> id(a) == id(b)    # 导入的模块 id 相同
    True
    >>> a.my_prop = 1     # 添加属性(简化,没用 hasattr 检查)
    >>> b.my_prop         # a 的属性 b自然是有的, 前面只是 as 么
    1

    # 2. 函数装饰器(闭包)
    >>> a = Worker_1('hello')
    hello
    >>> b = Worker_1()
    >>> id(a) == id(b)
    True

    # 3. 类装饰器单例
    >>> c = Worker_2('hi')
    hi
    >>> d = Worker_2()
    >>> id(c) == id(d)
    True

    # 4. __new__
    >>> e = Singleton_3_new('hi', name='you')
    ('hi',) {'name': 'you'}
    >>> f = Singleton_3_new()
    () {}
    >>> id(e) == id(f)
    True

    # 5. meta
    # >>> a = Worker_4('5',name='ha')
    # >>> b = Worker_4()
    # print('func', id(a) == id(b))
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)

    # 5. meta
    # print('-'*20)
    # a = Worker_4('5',name='ha')
    # b = Worker_4()
    # print('func', id(a) == id(b))