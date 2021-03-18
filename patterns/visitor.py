#!/usr/local/bin/python3
"""
*解说
目的是封装一些施加于数据结构上的操作. 操作需要修改的话, 接受操作的数据结构可以保持不变.
这样增加新的操作就很容易 -- 就是新增一个访问者类.

使用访问者模式时候, 要尽可能将更多的对象浏览逻辑放在防卫者类中, 不要放在子类中.
可以跨过多层结构, 访问属于不同层级结构的成员.

*本例
(算了 不画了)

*用途
- 电脑销售系统: 访问者(自己) --> 电脑配置系统(主板/CPU/内存...)
- 语法树, 维护抽象语法树中各个节点的行为.

*用例
- Python's ast.NodeVisitor: https://github.com/python/cpython/blob/master/Lib/ast.py#L250
which is then being used e.g. in tools like `pyflakes`.

- `Black` formatter tool implements it's own: https://github.com/ambv/black/blob/master/black.py#L71

*概述
从对象操作结构中分离算法
"""


class Node:
    pass


class A(Node):
    pass


class B(Node):
    pass


class C(A, B):
    pass


class D(C):
    pass


class Visitor:
    def visit(self, node, *args, **kwargs):
        meth = None
        for cls in node.__class__.__mro__:
            meth_name = f'visit_{cls.__name__}'
            meth = getattr(self, meth_name, None)
            if meth:
                break
        if not meth:
            meth = self.generic_visit
        return meth(node, *args, **kwargs)

    def generic_visit(self, node, *args, **kwargs):
        print(f'generic_visit {node.__class__.__name__}')

    def visit_B(self, node, *args, **kwargs):
        print(f'visit_B {node.__class__.__name__}')


def main():
    """
    >>> a, b, c, d = A(), B(), C(), D()
    >>> v = Visitor()

    >>> v.visit(a)
    generic_visit A

    >>> v.visit(b)
    visit_B B

    >>> v.visit(c)
    visit_B C

    >>> v.visit(d)
    visit_B D
    """

if __name__ == "__main__":
    # main()
    import doctest
    doctest.testmod(verbose=True)
