#!/usr/local/bin/python3
"""
*状态模式?
对象在其内部状态改变事, 改变他的行为, 就好像修改了类一样.
运行时根据状态改变行为, 每个条件分支放入到一个独立的类中, 这个对象不依赖其他
对象, 独立变化.

*本例
本例构建了一个FM/AM收音机, 可以在调频/调幅之间转换并调台.

传统的结构:
+-------------+  state                +-----------+
| Context     +<>-------------------->+ State     |
+-------------+                       +-----------+
| Request() o |                       | Handle()  |
+-----------^-+                       +-----+-----+
            |                               ^
            |                   +----------/_\---------+-- - - - -
            |                   |                      |
+-----------+-\         +-------+--------+     +-------+--------+
|state.Handle()|        | ConcreteStateA |     | ConcreteStateB |
+--------------+        +----------------+     +----------------+
                        | Handle()       |     | Handle()       |
                        +----------------+     +----------------+

本例的实现:
+----------------+  state             +-----------+
| Radio          +<>----------------->+ State     |
+----------------+                    +-----------+
| scan()         |                    | scan()    |
| toggle_amfm() o|                    +-----+-----+
+---------------^+                          ^
                |                   +----->/_\<--------+-- - - - -
                |                   |                  |
+---------------+----+      +-------+-------+     +----+----------+
| state.scan()       |      | AmState       |     | FmState       |
|      .toggle_amfm()|      +---------------+     +---------------+
+--------------------+      | toggle_amfm() |     | toggle_amfm() |
                            +---------------+     +---------------+


*用途:
- 人心情不同时的不同表现/行为
- 编钟
- 登录login logout

*参考
- https://github.com/faif/python_patterns
- http://ginstrom.com/scribbles/2007/10/08/design-patterns-python-style/

*概述
实现类的状态转换接口. 实现状态转换需要的超级类.
"""


class State:
    '''基本状态类, 用于共享功能(扫描 scan)'''

    def scan(self):
        '''扫描找下一个台'''
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        print(f'Scanning... Station is {self.stations[self.pos]} {self.name}')


class AmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ['1250', '1380', '1510']
        self.pos = 0
        self.name = 'AM'

    def toggle_amfm(self):
        print('Switching to FM')
        self.radio.state = self.radio.fmstate


class FmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ['81.3', '89.1', '103.9']
        self.pos = 0
        self.name = 'FM'

    def toggle_amfm(self):
        print('Switching to AM')
        self.radio.state = self.radio.amstate


class Radio:
    '''收音机, 有2个功能: 扫描(scan), 调频调幅(AM/FM)转换'''

    def __init__(self):
        '''存2个状态, 调频/调幅'''
        self.amstate = AmState(self)
        self.fmstate = FmState(self)
        self.state = self.amstate

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        self.state.scan()


def main():
    """
    >>> radio = Radio()

    # 注意这个精巧的测试构建方式
    >>> actions = [radio.scan]*2 + [radio.toggle_amfm] + [radio.scan]*2
    >>> actions *= 2

    >>> for action in actions:
    ...    action()
    Scanning... Station is 1380 AM
    Scanning... Station is 1510 AM
    Switching to FM
    Scanning... Station is 89.1 FM
    Scanning... Station is 103.9 FM
    Scanning... Station is 81.3 FM
    Scanning... Station is 89.1 FM
    Switching to AM
    Scanning... Station is 1250 AM
    Scanning... Station is 1380 AM
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
