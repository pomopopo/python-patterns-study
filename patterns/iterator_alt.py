#!/usr/local/bin/python3
"""
*干啥了
用 python 官宣的 iterator 协议来实现迭代.


*概述
通过容器, (逐个)访问容器内元素
"""


class NumberWords:
    _WORD_MAP = ('one', 'two', 'three', 'four', 'five')

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    # 一个具备迭代功能的类, 要实现 __iter__ 和 __next__ 两个属性方法

    def __iter__(self):
        return self

    def __next__(self):
        if self.start > self.stop or self.start > len(self._WORD_MAP):
            raise StopIteration
        current = self.start
        self.start += 1
        return self._WORD_MAP[current - 1]


def main():
    """
    # 一个正常的 1-2 迭代
    >>> for num in NumberWords(start=1, stop=2):
    ...     print(num)
    one
    two

    # 一个不太正常的迭代, 超范围的 stop 会激发 StopIteration, 终止迭代
    >>> for num in NumberWords(start=3, stop=7):
    ...     print(num)
    three
    four
    five

    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
