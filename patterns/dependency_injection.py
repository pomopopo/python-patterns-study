#!/usr/local/bin/python3
"""
*啥?!
依赖注入(DI)是一个对象提供依赖(服务)给另一个对象(客户)的技术.
作用: 解耦. 改变功能时, 客户无需改变代码 -- 换一个服务端就好了.(OCP原则)

*本例
分别对类初始化(init), 参数, 属性设置 3个方面做了注入 -- 依然使用高级函数特性

"""

import datetime
from typing import Callable


class ConstructorInjection:
    def __init__(self, time_provider: Callable) -> None:
        self.time_provider = time_provider

    def get_current_time_as_html_fragment(self):
        cur_time = self.time_provider()
        return f'<span class="tinyBoldText">{cur_time}</span>'


class ParameterInjection:
    def __init__(self) -> None:
        pass

    def get_current_time_as_html_fragment(self, time_provider: Callable) -> str:
        cur_time = time_provider()
        return f'<span class="tinyBoldText">{cur_time}</span>'


class SetterInjection:
    def __init__(self) -> None:
        pass

    def set_time_provider(self, time_provider: Callable):
        self.time_provider = time_provider

    def get_current_time_as_html_fragment(self):
        cur_time = self.time_provider()
        return f'<span class="tinyBoldText">{cur_time}</span>'


def production_code_time_provider():
    cur_time = datetime.datetime.now()
    return f'{cur_time.hour}:{cur_time.minute}'


def midnight_time_provider():
    return '24:01'


def main():
    """
    >>> t_CI_0 = ConstructorInjection(midnight_time_provider)
    >>> t_CI_0.get_current_time_as_html_fragment()
    '<span class="tinyBoldText">24:01</span>'

    >>> t_CI_now = ConstructorInjection(production_code_time_provider)
    >>> t_CI_now.get_current_time_as_html_fragment()
    '<span class="tinyBoldText">...</span>'

    >>> t_PI = ParameterInjection()
    >>> t_PI.get_current_time_as_html_fragment(midnight_time_provider)
    '<span class="tinyBoldText">24:01</span>'

    >>> t_SI = SetterInjection()
    >>> t_SI.get_current_time_as_html_fragment()
    Traceback (most recent call last):
    ...
    AttributeError: 'SetterInjection'...'time_provider'

    >>> t_SI.set_time_provider(midnight_time_provider)
    >>> t_SI.get_current_time_as_html_fragment()
    '<span class="tinyBoldText">24:01</span>'
"""

if __name__ == "__main__":
    # main()
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
