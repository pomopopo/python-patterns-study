#!/usr/local/bin/python3
"""
*共享状态单例(Borg)模式的用途?
Borg模式实现了一种 **共享状态** 的单例模式, 即多个实例之间共享同一状态, 关注的并
不是内存里只有一个该类的实例, 而是可以有多个实例.

*本例做了什么?
[预备知识] python类实例的 **属性**, 默认存在字典 __dict__ 里. 正常情况下, 每个
实例用自己字典. Borg模式把默认字典改为自有变量, 这样派生类就可以共享到同一个字典.

本例中, 把 __shared_state 设为默认字典, 属性就可以通过 __shared_state 进行共享.
设置时机: __init__ 时即可. and, 因为字典共享了, 所有属性都共享了!

+------------------+
|       Borg       |
+------------------+     +------------+
| __dict__ =       |<----+  YourBorg  |
|   __shared_state |     +------------+
+------------------+     | + state    |  状态,放在 __shared_state 字典里
                         | + __str__  |
                         +------------+
                            |      |
                        +-----+  +-----+
                        | rm1 |  | rm2 |
                        +-----+  +-----+
            共享修改状态  |state|  |state|
                        +-----+  +-----+

*常见使用场景?
- 管理数据库连接, 有用.
https://github.com/onetwopunch/pythonDbTemplate/blob/master/database.py
- 多线程的线程池
- 操作系统的文件系统
- 应用程序的日志
- 软件自身的ini/cfg配置管理

*要点
- 修改了属性字典 __ dict __ ,所以所有实例都拥有相同的字典
- 同类实例修改属性，同步修改属性值
- 虽然分享状态，但是同类实例的 id 并不相同

*与单例(Singleton)模式的异同
- 异: Borg 实例的地址不同, Singleton 实例地址相同
- 异: Singleton只有一个地址, 比较节省内存
- 同: 属性都共享

*参考:
- https://www.github.com/faif/design-patterns
- https://blog.csdn.net/qq_33961117/article/details/90604014

*八卦一下
Borg 这个词来自于 Star Trek 里边的一个外星种族, 首脑可以下发指令, 成员间共享
一切信息. 通常是邪恶的代名词.(http://catb.org/jargon/html/B/Borg.html)

*概述
多实例间提供类似于单例模式的状态共享.
"""


class Borg:
    _shared_state = {}

    def __init__(self):
        # 核心: 重写属性字典
        self.__dict__ = self._shared_state


class YourBorg(Borg):
    def __init__(self, state=None):
        super().__init__()
        if state:
            self.state = state
        else:
            # 给第一个实例化的, 设定个初始值
            if not hasattr(self, "state"):
                self.state = "Init"

    def __str__(self):
        return self.state


def main():
    """
    >>> rm1 = YourBorg()
    >>> rm2 = YourBorg()

    >>> rm1.state = 'Idle'
    >>> rm2.state = 'Running'

    >>> print('rm1: {0}'.format(rm1))
    rm1: Running
    >>> print('rm2: {0}'.format(rm2))
    rm2: Running

    # 修改 rm2 的 .state 属性的话, rm1 的属性也随之被改变
    >>> rm2.state = 'Zombie'

    >>> print('rm1: {0}'.format(rm1))
    rm1: Zombie
    >>> print('rm2: {0}'.format(rm2))
    rm2: Zombie

    # rm1 和 rm2 的 id 并不相同
    >>> rm1 is rm2
    False

    # 再新建实例, 也会得到现有的状态
    >>> rm3 = YourBorg()

    >>> print('rm1: {0}'.format(rm1))
    rm1: Zombie
    >>> print('rm2: {0}'.format(rm2))
    rm2: Zombie
    >>> print('rm3: {0}'.format(rm3))
    rm3: Zombie

    # 创建新实例可以设定状态
    >>> rm4 = YourBorg('Running')

    >>> print('rm4: {0}'.format(rm4))
    rm4: Running

    # 然后, 所有实例的状态都会被改变
    >>> print('rm3: {0}'.format(rm3))
    rm3: Running
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()
