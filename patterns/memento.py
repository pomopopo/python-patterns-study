#!/usr/local/bin/python3
"""
*意图:
在不破坏封装的前提下, 捕获一个对象的内部状态, 并在该对象之外保存这个状态.
后续可以将该对象恢复到事先保存的状态.

*适用性:
保存, 需要时恢复.
如果用接口获得其状态, 则会暴露对象实现细节, 破坏封装.

*各个角色做做什么?
- 发起人:
    1, 创建汉语当前状态的备忘录对象
    2, 使用备忘录对象存储其内部状态
- 备忘录:
    1, 存发起人对象的内部状态, 可以根据发起人搬到存多少个内部状态
    2, 备忘录可以保护其内容不被发起人之外的任何对象获取
- 负责人:
    1, 负责保存备忘录对象
    2, 不检查备忘录对象的内容

*场景
备份系统时
GHOST

*参考
http://code.activestate.com/recipes/413838-memento-closure/


*概述
给对象提供恢复之前状态的能力.
"""

from copy import deepcopy, copy


def memento(obj, deep=False):
    state = deepcopy(obj.__dict__) if deep else copy(obj.__dict__)

    def restore():
        obj.__dict__.clear()
        obj.__dict__.update(state)

    return restore


class Transaction:
    deep = False
    states = []

    def __init__(self, deep, *targets):
        self.deep = deep
        self.targets = targets
        self.commit()

    def commit(self):
        self.states = [memento(target, self.deep) for target in self.targets]

    def rollback(self):
        for a_state in self.states:
            a_state()


class Transactional:
    def __init__(self, method):
        self.method = method

    def __get__(self, obj, T):
        def transaction(*args, **kwargs):
            state = memento(obj)
            try:
                return self.method(obj, *args, **kwargs)
            except Exception as e:
                state()
                raise e
        return transaction


class NumObj:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.value!r}>'

    def inc(self):
        self.value += 1

    @Transactional
    def do_stuff(self):
        self.value = '1111'
        self.inc()


def main():
    """
    >>> n = NumObj(-1)
    >>> n
    <NumObj: -1>

    >>> a_trans = Transaction(True, n)
    >>> try:
    ...     for i in range(3):
    ...         n.inc()
    ...         print(n)
    ...     a_trans.commit()
    ...     print('-- committed')
    ...     for _ in range(3):
    ...         n.inc()
    ...         print(n)
    ...     n.value += 'x'
    ...     print(n)
    ... except Exception:
    ...     a_trans.rollback()
    ...     print('-- rolled back')
    <NumObj: 0>
    <NumObj: 1>
    <NumObj: 2>
    -- committed
    <NumObj: 3>
    <NumObj: 4>
    <NumObj: 5>
    -- rolled back

    >>> n
    <NumObj: 2>

    >>> try:
    ...     n.do_stuff()
    ... except Exception:
    ...     print('-> do_stuff failed')
    ...     import sys
    ...     import traceback
    ...     traceback.print_exc(file=sys.stdout)
    -> do_stuff failed
    Traceback (most recent call last):
    ...
    TypeError: ... str (not "int") to str

    >>> n
    <NumObj: 2>

"""

if __name__ == "__main__":
    main()
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
