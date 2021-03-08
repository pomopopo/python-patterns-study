#!/usr/local/bin/python3
"""
*做什么用?
动态添加功能到现有对象上, 无需修改其实现. 与继承不同, 功能特性只加在某一
个特定的类上, 并没有加在整个子类上.

*本例做什么了?
本例展示了一种给文字添加特定标签(<b>和<i>), 进行格式化的的方法. 同时装饰
器可以连续使用----调用一个之后, 可以外面包着另一个.

*用途?
Grok 框架用在了权限和事件接收上:
http://grok.zope.org/doc/current/reference/decorators.html

*参考

*概述
不影响原类情况下添加功能特性.
"""


class TextTag:
    def __init__(self, text):
        self._text = text

    def render(self):
        return self._text


class BoldWrapper(TextTag):
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def render(self):
        return f'<b>{self._wrapped.render()}</b>'


class ItalicWrapper(TextTag):
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def render(self):
        return f'<i>{self._wrapped.render()}</i>'


def main():
    """
    >>> simple_hello = TextTag('hello, wolrd.')
    >>> special_italic = ItalicWrapper(simple_hello)
    >>> special_bold = BoldWrapper(simple_hello)
    >>> special_hello = ItalicWrapper(BoldWrapper(simple_hello))

    >>> for i in (simple_hello, special_italic, special_bold, special_hello):
    ...     print(i.render())
    hello, wolrd.
    <i>hello, wolrd.</i>
    <b>hello, wolrd.</b>
    <i><b>hello, wolrd.</b></i>
    """


if __name__ == "__main__":
    # main()
    import doctest
    doctest.testmod(verbose=True)
