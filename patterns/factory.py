#!/usr/local/bin/python3
"""
*工厂模式干啥的?
从工厂对象生产出其他对象.

*本例做什么的?
本例子展示了一种英语本地化为两种语言的方法: 英语和希腊语.
get_localizer() 是一个 **工厂函数**, 它根据所选的语言, 返回不同的本地化解释器.
根据需要本地化语言不同, 解释器会返回 **不同的类实例**. 同时, 调用的主代码无需担心
具体哪个本地语言被实例化, 因为"本地化"的调用命令是一样的.

                        +--------------+
                        |   GreekLoca  |
                    +---+--------------+
+---------------+   |   | + __init__   |
|get_localizer()|   |   | + localizer()|
|...            |   |   +--------------|
|return Obj <-------+
+---------------+   |   +--------------+
                    +---+  EgnlishLoca |
                        +--------------+
                        | + __init__   |
                        | + localizer()|
                        +--------------+

*哪里会用到?
工厂模式可以(经常)在 Django 框架中见到.
http://django.wikispaces.asu.edu/*NEW*+Django+Design+Patterns
例如, 表单页面的主题和信息字段是从同一个表单工厂(CharField)继承来的, 然而能够
根据不同目的得到不同实现.

动物工厂，根据动物叫声的不同而实例化为猫类或狗类。

- 实现解耦. 创建和使用分离, 需要不同实例的时候, 更容易扩展
- 创建和使用分离, 使用者不需要知道创建过程, 只需要使用即可.
- 降低代码重复. 如果工厂的代码比较复杂, 能省很多
- 创建过程统一由工厂管理, 利于后续修改
- 被创建对象的生命周期需要统一管理, 要保证在整个程序中的行为一致性(?)

*References:
- https://www.github.com/faif/design-patterns

*概述
不需要指定确切的类,就可以创建实例.
"""


class GreekLocalizer:
    """Greek 语言类, 最简单的翻译官."""

    def __init__(self) -> None:
        self.translations = {"dog": "σκύλος", "cat": "γάτα"}

    def localize(self, msg: str) -> str:
        """没有翻译的,就直接原样返回"""
        return self.translations.get(msg, msg)


class EnglishLocalizer:
    """English 语言类, 直接返回原信息"""

    def localize(self, msg: str) -> str:
        return msg


def get_localizer(language: str = "English") -> object:
    """工厂函数! 可以选择语种 English/Greek"""

    # 核心:工厂的对应关系
    localizers = {
        "English": EnglishLocalizer,
        "Greek": GreekLocalizer,
    }
    # 返回实例对象
    return localizers[language]()


def main():
    """
    # 分别创建2个本地化器
    >>> e, g = get_localizer(language="English"), get_localizer(language="Greek")

    # 翻译几个词
    >>> for msg in "dog parrot cat bear".split():
    ...     print(e.localize(msg), g.localize(msg))
    dog σκύλος
    parrot parrot
    cat γάτα
    bear bear
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()