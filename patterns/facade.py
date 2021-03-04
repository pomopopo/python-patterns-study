#!/usr/local/bin/python3
"""
*干啥呀?
门面模式为复杂系统提供了一种简化接口的方式, 通过提供单一入口, 访问系统底层功能
会变得更简单. 这类抽象在很多实际生活中比较常见. 例如, 打开电脑只需要按一下电源
键, 但实际上背后发生了很多操作(如从磁盘载入程序到内存), 这种情况下, 电源键就起
到了为开机的所有底层过程提供了单一接口的作用.

*练练?
例如标准库的 isdir() 函数, 用户只想知道该路径是不是文件夹, 但系统要做很多操作,
并调用其他模块(如: os.stat), 才能给出答案.

*咋办的?
模拟了一台计算机, 组装起来, start() 实现一键开机.

                                            +--------------+
                +-------------------+   +-->+     CPU      |
                |   ComputerFacade  |   |   +--------------+
                +-------------------+   |   |    freez()   |
                |                   |   |   |    jump()    |
                |   cpu o---------------+   |    execute() |
+-----------+   |   ram o----------------+  +--------------+
|  client   |   |   ssd o--------------+ |
+-----------+   |                   |  | |  +--------------+
|  start() -------> start()         |  | +->+     RAM      |
+-----------+   |     cpu.freeze()  |  |    +--------------+
                |     ram.load()    |  |    |    load()  -------+
                |     cpu.jump()    |  |    +--------------+    |
                |     cpu.execute() |  |                        |
                |                   |  |    +--------------+    |
                |                   |  +--->+     SSD      |    |
                +-------------------+       +--------------+    |
                                            |    read()  <------+
                                            +--------------+


*谁家的娃呀?
- 数据库 JDBC 的应用
- session 的应用

*瞅啥?
https://github.com/faif/python_patterns
https://blog.csdn.net/longronglin/article/details/1454315

*概述
为复杂系统提供简单统一的接口.
"""

# 先来些电脑的零部件


class CPU:
    '''模拟CPU, 能暂停, 调整PC指针, 执行'''

    def freeze(self):
        print('Freezing processor.')

    def jump(self, position):
        print('Jumping to:', position)

    def execute(self):
        print('Executing.')


class RAM:
    '''模拟内存, 能加载'''

    def load(self, position, data):
        print(f'Loading "{data}" from "{position}".')


class SSD:
    '''模拟固态硬盘, 能读数据'''

    def read(self, lba, size):
        return f'some data from {lba} with zize {size}'


# 然后是零部件组装


class ComputerFacade:
    '''把一大堆零件组装成计算机'''

    def __init__(self) -> None:
        self.cpu = CPU()
        self.ram = RAM()
        self.ssd = SSD()

    def start(self):
        self.cpu.freeze()
        self.ram.load('0x00', self.ssd.read('0x100', '1024'))
        self.cpu.jump('0x00')
        self.cpu.execute()


if __name__ == "__main__":
    """
    >>> my_laptop = ComputerFacade()
    >>> my_laptop.start()
    Freezing processor.
    Loading "some data from 0x100 with zize 1024" from "0x00".
    Jumping to: 0x00
    Executing.
    """

    import doctest
    doctest.testmod(verbose=True)
