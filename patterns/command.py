#!/usr/local/bin/python3
"""
*是啥
命令模式将命令激活和执行者分离开, GoF 里边比较好的例子是"菜单项":
有个菜单, 里边有很多菜单项, 每个菜单项点选的时候, 都要执行一定的操作,
因此, 每个菜单项都要传递一个有可执行动作的命令对象进去.

*能干啥
- 对请求排队和记录请求日志，
- 支持可撤销的操作

*本例
本例添加了2个菜单项, 每个都可以接受一个文件名, 或隐藏, 或删除, 也提供了undo功能.
每个菜单项类可以接受相应的输入, 并在选中(press)的时候执行命令.

客户端 -- 请求者 -- 命令角色 -- 具体命令 -- 接受者


*谁用了?
- python生态中就有, django HttpRequest 有用到:
https://docs.djangoproject.com/en/2.1/ref/request-response/#httprequest-objects

*概述
实现面向对象的函数回调
"""


class HideFileCommand:
    def __init__(self):
        self._hidden_files = []

    def execute(self, filename):
        print(f'hiding {filename}')
        self._hidden_files.append(filename)

    def undo(self):
        filename = self._hidden_files.pop()
        print(f'un-hiding {filename}')


class DeleteFileCommand:
    def __init__(self):
        self._deleted_files = []

    def execute(self, filename):
        print(f'deleting {filename}')
        self._deleted_files.append(filename)

    def undo(self):
        filename = self._deleted_files.pop()
        print(f'restoring {filename}')


class MenuItem:
    def __init__(self, command):
        self._command = command

    def on_do_press(self, filename):
        self._command.execute(filename)

    def on_undo_press(self):
        self._command.undo()

if __name__ == "__main__":
    item1 = MenuItem(DeleteFileCommand())
    item2 = MenuItem(HideFileCommand())
    fn = 'test-file'
    item1.on_do_press(fn)
    item1.on_undo_press()

    item2.on_do_press(fn)
    item2.on_undo_press()
