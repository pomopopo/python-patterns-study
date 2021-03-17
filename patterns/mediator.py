#!/usr/local/bin/python3
"""
*调停者/中间人,作甚了?
包装一系列对象的相互作用方式, 使对象间相互作用不明显, 实现松耦合.
当某些对象间的相互作用发生改变时, 不会立即影响其他对象间的作用.

    /----------/                  mediator /-----------/
    / Mediator /<--------------------------/ Colleague /
    /---+-----/                            /----+------/
        ^                                       ^
        |                                       |
        |                          +------------+--------------+
        |                          |                           |
+-------+----------+    +----------+----------+                |
| ConcreteMediator +--->+ ConcreteColleague_1 | +              |
+---------------+--+    +---------------------+ |              |
                |          +--------------------+   +----------+----------+
                +---------------------------------->+ ConcreteColleague_2 |
                                                    +---------------------+

*应用场景
- 法院 / 原告 / 被告
- 一组对象封装挺好的, 但是通信方式复杂 or 依赖关系复杂时, 可用
- 一个对象引用很多其他对象, 并且直接与这些对象通信, 就很难复用该对象时
- 想定制一个分部在多个类中的行为, 但又不想生成太多子类.

*辨证
Mediator vs Facade
- Mediator
    - Mediator 对同事之间的通信进行抽象, 集中不属于 *任何* 单个对象的功能.
    - Mediator 封装复杂协议之后, 提供新的语义.
    - Mediator 的同事对象知道中介, 并与中介通信, 不直接联系其他同事.
- Facade
    - Facade 对子系统对象的接口进行抽象, 使之更容易使用
    - 协议是单向的, Facade 对子系统单向提出请求, 反之不行.
    - 不定义新功能, 子系统也不知道 Facade 的存在
    - 一般说只需要一个 Facade 对象, 因此该 Facade 对象也是 Singleton

*参考
- github.com/faif/python-patterns
- https://www.cnblogs.com/Liqiongyu/p/5916710.html
- https://blog.csdn.net/longronglin/article/details/1454315

*概要
封装一组对象间的交互
"""


class Chatroom:
    '''中间人'''
    def display_msg(self, user, message):
        print(f'[{user}]: {message}')


class User:
    '''实例化之后, 需要互相交换的一组类'''
    def __init__(self, name):
        self.name = name
        self.chat_room = Chatroom()

    def say(self, message):
        self.chat_room.display_msg(self, message)

    def __str__(self):
        return self.name


def main():
    """
    # 建一组类
    >>> molly = User('Molly')
    >>> mark = User('Mark')
    >>> ethan = User('Ethan')

    # 交互部分
    >>> molly.say('hi team!')
    [Molly]: hi team!

    >>> mark.say('roger')
    [Mark]: roger

    >>> ethan.say('yep')
    [Ethan]: yep
    """

if __name__ == "__main__":
    # main()

    import doctest
    doctest.testmod(verbose=True)
