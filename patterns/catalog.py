#!/usr/local/bin/python3
"""
*说明
一个类在初始化的时候, 通过参数指定不同的函数.
注意: 这里用字典维护了多种情况.

*本例
本例实现了 4 种方法啊!!!

"""

__author__ = "Ibrahim Diop <ibrahim@sikilabs.com>"


class Catalog:
    '''第一种: 最简单, 最直接的办法'''

    def __init__(self, param):
        # 用字典设定对应关系, 也可以存其他可能参数
        self._static_method_choices = {
            'p1': self._static_method_1,
            'p2': self._static_method_2,
        }

        # 检查参数
        if param in self._static_method_choices:
            self.param = param
        else:
            raise ValueError(f'Invalid Value for Param: {param}')

    @staticmethod
    def _static_method_1():
        print('exec method 1')

    @staticmethod
    def _static_method_2():
        print('exec method 2')

    def main_method(self):
        '''根据 self.param 来执行 _static_method_1 或者 _static_method_2'''
        self._static_method_choices[self.param]()


class CatalogInstance:
    '''第二种: 调用略麻烦, 但是不用 @staticmethod 修饰了'''

    def __init__(self, param):
        self.x1 = 'x1'
        self.x2 = 'x2'
        if param in self._instance_method_choices:
            self.param = param
        else:
            raise ValueError(f'Invalid Value for Param: {param}')

    def _instance_method_1(self):
        print(f'Value {self.x1}')

    def _instance_method_2(self):
        print(f'Value {self.x2}')

    _instance_method_choices = {
        'p1': _instance_method_1,
        'p2': _instance_method_2,
    }

    def main_method(self):
        self._instance_method_choices[self.param].__get__(self)()


class CatalogClass:
    '''第三种: 调用时更麻烦一点, 而且还要 @classmethod 修饰'''
    x1 = 'x1'
    x2 = 'x2'

    def __init__(self, param):
        if param in self._class_method_choices:
            self.param = param
        else:
            raise ValueError(f'Invalid Value for Param: {param}')

    @classmethod
    def _class_method_1(cls):
        print(f'Value {cls.x1}')

    @classmethod
    def _class_method_2(cls):
        print(f'Value {cls.x2}')

    _class_method_choices = {
        'p1': _class_method_1,
        'p2': _class_method_2,
    }

    def main_method(self):
        self._class_method_choices[self.param].__get__(None, self.__class__)()


class CatalogStatic:
    '''第四种: 麻烦的很, 无论是函数装饰, 还是最终调用'''

    def __init__(self, param):
        if param in self._static_method_choices:
            self.param = param
        else:
            raise ValueError(f'Invalid Value for Param: {param}')

    @staticmethod
    def _static_method_1():
        print('exec method 1')

    @staticmethod
    def _static_method_2():
        print('exec method 2')

    _static_method_choices = {
        'p1': _static_method_1,
        'p2': _static_method_2,
    }

    def main_method(self):
        self._static_method_choices[self.param].__get__(None, self.__class__)()



def main():
    """
    >>> test = Catalog('p2')
    >>> test.main_method()
    exec method 2

    >>> test = CatalogInstance('p1')
    >>> test.main_method()
    Value x1

    >>> test = CatalogClass('p2')
    >>> test.main_method()
    Value x2

    >>> test = CatalogStatic('p1')
    >>> test.main_method()
    exec method 1

"""
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
