#!/usr/local/bin/python3
"""
*迭代器
顺序访问元素而不暴露内部细节

*用生成器实现迭代器
python么, 生成器, 迭代器都很丰富的, 可用.

*每天一个小常识
yield 和 yield from
- yield 返回一个        相当于子程序的中断关键字
- yield from 返回一堆   是委托生成器的管道, 把后面的可迭代对象逐个引入到管道里
- yield from = for xxx in yyy: yield xxx

*用途
- 查数据库,返回结果集(map, list, set)

*概述
yield 的容器, 逐个访问内部元素
"""


def count_to(count):
    numbers = ['one', 'two', 'three', 'four', 'five', ]
    yield from numbers[:count]


def count_to_two():
    return count_to(2)


def count_to_five():
    return count_to(5)


def main():
    """
    >>> count_to_two()
    <generator object count_to at 0x...>

    >>> list(count_to_two())
    ['one', 'two']

    >>> for n in count_to_two():
    ...    print(n)
    one
    two

    >>> for n in count_to_five():
    ...    print(n)
    one
    two
    three
    four
    five

    """


if __name__ == "__main__":

    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
