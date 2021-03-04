#!/usr/local/bin/python3
"""
*原型模式能做嘛子?
本模式可用于减少应用程序所需要类的数量. 在创建新实例的时候, 不依赖于子类,
而是通过在 "运行时" 拷贝原型的实例来实现.

当实例类只有 *有限的* 几种组合状态, 且实例化成本很高时, 在需要衍生新类型
的对象的时候, 原型就比较有用了.

*本例在弄撒子嘞?
当一个应用中的原型数量可以变化的时候, 保留一个调度器 (Dispatcher) 就有用
(注册器, 管理器 都一样). 这样允许客户端在克隆新实例之前, 可以向调度器请求.

下面提供了一个调度器的例子, 包含3个原型的拷贝:
    默认(default),
    类a(object-a),
    类b(object-b).

+--------------+             +---------+ register
|  Prototype   <--prototype--+ default +-----+
+--------------+             +---------+     |
|  + clone()   |                             |
+-----------^--+                             |
            |prototype           +-----------v-----------+
 +-------------------+           |      Dispatcher       |
 |     object-a      |           +-----------------------+
 +-------------------+           |  _objects={}          |           Client
 |   value='a-value' +--register->  get_objects()    o-------- n,p=prototype.clone()
 |   category='a'    |           |  register_objects()   |
 +----------^--------+           |  unregister_objects() |
            |clone()             +-----------^-----------+
    +-------------------+                    |
    |     object-b      +----register--------+
    +-------------------+
    |   value='b-value' |
    |   is_checked=True |
    +-------------------+

*应用场景?
- 数据库操作, 在创建后缓存起来, 在需要请求的时候返回一个克隆, 可以减少调用.
- 避免创建与产品平行层次的工厂类时.
- 当一个类的实例只能有几个不同状态组合中的一种时, 建立响应数目的原型, 并克隆
可能比每次用合适的状态手工实例化该类更方便一些.
- 类初始化需要非常多的资源(数据/硬件资源etc)
- 性能和安全要求的场景
- new一个对象需要非常繁琐的数据准备或者访问权限时
- 一个对象需要多个修改者时
- 很少单独出现, 一般与工厂方法一起出现, clone 的结果由工厂方法提供给调用者

*优缺点
- 优点:  性能提高; 构造函数的消耗就一次.
- 缺点:  功能要通盘考虑;
        已有类不一定可改造: 不支持串行化的/含循环引用的;
        必须实现clone接口

*概述
克隆原型, 可得新实例.(相当于浅拷贝)
"""

from typing import Any, Dict


class Prototype:
    def __init__(self, value: str = 'default', **attrs: Any) -> None:
        self.value = value
        self.__dict__.update(attrs)

    def clone(self, **attrs: Any) -> None:
        """克隆原型, 更新自家的属性字典"""
        # 也可以通过 copy.deepcopy 来实现
        obj = self.__class__(**self.__dict__)
        obj.__dict__.update(attrs)
        return obj


class PrototypeDispatcher:
    def __init__(self) -> None:
        self._objects = {}

    def get_objects(self) -> Dict[str, Prototype]:
        return self._objects

    def register_object(self, name: str, obj: Prototype) -> None:
        self._objects[name] = obj

    def unregister_object(self, name: str) -> None:
        del self._objects[name]


def main():
    """
    >>> dispatcher = PrototypeDispatcher()
    >>> prototype = Prototype()

    >>> d = prototype.clone()
    >>> a = prototype.clone(value='a-value', category='a')
    >>> b = a.clone(value='b-value', is_checked=True)
    >>> dispatcher.register_object('object-a', a)
    >>> dispatcher.register_object('object-b', b)
    >>> dispatcher.register_object('default', d)

    >>> for n, p in dispatcher.get_objects().items():
    ...     print(n, p.value)
    object-a a-value
    object-b b-value
    default default

    >>> print(b.category, b.is_checked)
    a True
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
    # main()
