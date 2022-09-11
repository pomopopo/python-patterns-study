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

+--------------------+
| Singleton1(Wrapper)| 函数闭包的例子
+--------------------+
| - _instances={}    |
| + wrapper() o----------- return _instances[cls]
+--------------------+

+--------------------+
| Singleton2(Class)  | 类装饰器的例子
+--------------------+
|  - _instances={}   |
|  + __call__() o--------- return _instances[self._cls]
+--------------------+

*常见使用场景?
- 替代全局变量, 系统只需要一个实例对象那种. 例如: 序列号生成器/资源管理器
- 只允许一个访问点, 除了该点,不能通过其他途径访问.

*要点
- 如果实例不存在, 就创建一个新的; 如果实例存在, 就返回已创建的实例.
- 注意多线程下, 要加锁(效率低), 要么加同步(效率可以)

*优缺点
- 优点:  唯一实例, 受控访问;
        因为只有一个对象, 节约资源----尤其那些需要频繁创建/销毁的对象;
        也可以改成指定个数的实例, 效率能高些.
- 缺点:  单例很难扩展----没有抽象层;
        职责过重, 违背了单一职责, 对象的创建和功能耦合为一的;
        实例化的共享对象长时间不用的话, 有的语言会 GC 掉, 导致状态丢失.

*参考
https://blog.csdn.net/weixin_39309402/article/details/98126883

*概述 TL;DR
确保某类只有一个实例.
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

# """ 用函数闭包实现功能完整的单例，functools 实现对单例的封装，threading 实现同步锁，可以线程安全"""
import functools
import threading


def singleton_0_func_wrap(cls):
    """from 官方建议的实现方式，对类的支持比较完善"""
    cls.__new_original__ = cls.__new__

    @functools.wraps(cls.__new__)
    def singleton_new(cls, *args, **kwargs):
        # Lock 保证线程安全。CAUTION: 非必要情况启用线程锁会启动 GIL，拖慢运行速度
        with threading.Lock():
            it = cls.__dict__.get('__it__')
            if it is not None:
                return it
            cls.__it__ = it = cls.__new_original__(cls, *args, **kwargs)
            it.__init_original__(*args, **kwargs)
            return it

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__
    return cls


@singleton_0_func_wrap
class Worker_0(object):

    def __new__(cls, *args, **kwargs):
        cls.x = 10
        return object.__new__(cls)

    def __init__(self, x, y):
        assert self.x == 10
        self.x = x
        self.y = y


# """用函数闭包实现单例"""
def singleton_1_func_wrap(cls):
    """这个函数比较简单，不支持 worker class 的 __new__ 或者继承"""
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

    def __new__(cls, *args, **kwargs):
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
    # 0. 函数装饰器的线程安全单例

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


    # 对线程安全的函数装饰器单例测试，看打印结果
    def worker0():
        s = Worker_0(3, 7)
        print(id(s))


    tasks = [threading.Thread(target=worker0) for _ in range(5)]
    [t.start() for t in tasks]
    [t.join() for t in tasks]
