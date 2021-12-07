#!/usr/local/bin/python3
"""
*用途
用面向对象的方式实现 if ... elif ... elif ... else ... 分支.
益处: 条件--对应动作可以运行时动态调整.

本模式用于把请求 *发送方* 和 *接收方* 解耦, 请求可以沿着 *一串*
接收者传递, 直到被处理.

客户端无需知道(其实也真不知道)具体是哪个环节处理的(没提供位置机制),
处理者要么承担责任, 要么推给下家--所以一个请求最终没人理也是有可能的.

接收方为求简便, 保留了下一步骤的引用, 有的接收方能发送请求到多个方向,
这样就构成了"责任树"

经常与 Composite 模式联用: 构件的父构件可以作为它的后继

*本例解析

                                    +----------------+
                                    |                |
                        +-----------v---+  successor |
+------+                |Handler        +------------+
|client+--------------->----------------+
+------+                |  <<virtual>>  |
                        |HandleRequest()|
                        +-------+-------+
                                ^
        +---------------------+-+-----------------------+
        |                     |                         |
+-------+--------+    +-------+--------+        +-------+-------+
|ConcreteHandler0|    |ConcreteHandler1|        |FallbackHandler|
+----------------+    +----------------+  ...   +---------------+
|HandleRequest() |    |HandleRequest() |        |HandleRequest()|
+----------------+    +----------------+        +---------------+

实例的话, 链式调用过程
+--------------+
| aClient      |    +------------------+
+--------------+    | aConcreteHandler |    +------------------+
| aHandler  o-----> +------------------+    | aConcreteHandler |
+--------------+    | successor     o-----> +------------------+
    data = 2~35     +------------------+    | successor      o-----> ...
                        handle 0~10         +------------------+
                                                handle [10,20)

*典型例子
成语接龙(马到成功--功不可没--没齿难忘)

*概要
让请求沿着接受链传递, 直至有人处理.
"""

from abc import ABC, abstractmethod


class Handler(ABC):
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, request):
        '''处理请求.
        处理并结束, 或者传给下家.
        有时候么, 哪怕成功处理了, 也传给下家.
        '''
        res = self.check_range(request)
        if not res and self.successor:
            self.successor.handle(request)

    @abstractmethod
    def check_range(self, request):
        '''具体工作的虚拟方法'''


class ConcreteHandler0(Handler):
    '''每个handler都应该简单/稳定.'''
    @staticmethod
    def check_range(request):
        if 0 <= request <= 10:
            print(f'Request {request} handled in handler 0')
            return True


class ConcreteHandler1(Handler):
    '''自带内部状态的'''
    start, end = 10, 20

    def check_range(self, request):
        if self.start <= request < self.end:
            print(f'request {request} handled in handler 1')
            return True


class ConcreteHandler2(Handler):
    '''从辅助函数获取数据的'''

    def check_range(self, request):
        start, end = self.get_interval_from_db()
        if start <= request < end:
            print(f'request {request} handled in handler 2')
            return True

    @staticmethod
    def get_interval_from_db():
        return (20, 30)


class FallbackHandler(Handler):
    '''终结者'''
    @staticmethod
    def check_range(request):
        print(f'end of request, no handler for {request}')
        return False


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)

    h0 = ConcreteHandler0()
    h1 = ConcreteHandler1()
    h2 = ConcreteHandler2(FallbackHandler())

    h0.successor = h1
    h1.successor = h2

    requests = [2, 5, 14, 22, 18, 3, 35, 27, 20]
    for r in requests:
        h0.handle(r)
