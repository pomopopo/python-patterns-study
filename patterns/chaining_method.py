#!/usr/local/bin/python3
"""
*链式?
链式调用是python常见的方式, 例如 str 的所有相关函数, 因为调用之后又返回了 str 对象.
当需要一个物体做很多动作(操作)的时候, 链式可以省去很多创建变量的过程.

*本例?
实现了一个人(Person)可以链式调用动作(Action)里的一种, 执行到 stop 时不可继续调用.

*责任链和链式调用是两码事
责任链: 相当于 if ... elif ... elif ... , 链中的类, 可以指定自己的下一步是谁
链式调用: 自己用"."调用自己的方法/属性

*特点?
链式方便调用过程, 用 "." 连接即可
"""


class Person:
    def __init__(self, name, action):
        self.name = name
        self.action = action

    # 返回的 action 可以链式调用的
    def do_action(self):
        print(self.name, self.action.name, end='\n')
        return self.action


class Action:
    def __init__(self, name):
        self.name = name

    # 返回 self 就可以链式调用
    def amount(self, val):
        print(val, end='\n')
        return self

    def stop(self):
        print('STOP')


if __name__ == "__main__":
    """
    >>> mv = Action('move')
    >>> ps = Person('Jack', mv)
    # 高光时刻到来, 链式调用, 走起!
    >>> ps.do_action().amount('5m').stop()
    Jack move
    5m
    STOP
    """

    import doctest
    doctest.testmod(verbose=True)
