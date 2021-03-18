#!/usr/local/bin/python3
"""
*是啥?
继承者都会留下注册信息

*本例做了?
造一注册表存储器类, 派生出"已注册类的基类" BaseRegisteredClass,
其他子类即可从已注册类的基类派生, 新增的子类就会被记录到注册表存储器
的 REGISTRY 字典中.

                    +----------------+
                    | RegistryHolder |
                    +----------------+
                    | REGISTRY       | 这里放注册表, new 的时候更新
                    +-------+--------+
                            ^
                +-----------+-----------+
                |  BaseRegisteredClass  | 这个才是基类, 全空, 其他人从这里继承
                +---+---------------+---+
                    ^               ^
+-------------------+-+          +--+------------------+
| ConcreteRegistree_1 |          | ConcreteRegistree_2 |
+---------------------+          +---------------------+
    ClassRegistree                      Regi_2

*能干啥?
(dunno)

"""


class RegistryHolder(type):

    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)

        # 用类名做字典键值. 也可以用类的其他参数, 但方便程度差点
        cls.REGISTRY[new_cls.__name__] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)


class BaseRegisteredClass(metaclass=RegistryHolder):
    """
    从这里继承的类, 都会包含 RegistryHolder.REGISTRY 字典,
    该字典构成为 {类名: 类本身, ...}
    """


def main():
    """
    # 增加子类之前
    >>> sorted(RegistryHolder.REGISTRY)
    ['BaseRegisteredClass']

    # 增加一个新子类
    >>> class ClassRegistree(BaseRegisteredClass):
    ...     def __init__(self, *args, **kwargs):
    ...        pass

    # 增加子类之后, REGISTRY 有变化
    >>> sorted(RegistryHolder.get_registry())
    ['BaseRegisteredClass', 'ClassRegistree']

    # 子类再子类, 何如?
    >>> class Regi_2(ClassRegistree):
    ...     pass
    >>> sorted(RegistryHolder.REGISTRY)
    ['BaseRegisteredClass', 'ClassRegistree', 'Regi_2']
    """


if __name__ == "__main__":
    # main()
    import doctest
    doctest.testmod(verbose=True)
