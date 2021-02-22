#!/usr/local/bin/python3
"""
*抽象工厂模式的用处?

    在一些语言里(例如 Java), 抽象工厂模式提供了无需修改原 class 就能
创建新对象(相关/依赖)的接口.

    思路就是: 根据业务逻辑/平台选择等, 把 **创建对象** 这件事抽象出来.

    抽象工厂是工厂的升级版,工厂模式只能生产一个等级的产品,抽象工厂生产多
个等级的产品.

    python 中, 我们用的接口就是个简单的可调用对象, 这是python的内置
(builtin) 接口, 在正常情况下, 我们可以简单地降类作为可调用对象----类
在python中是第一类对象.

*本例做了什么?
    抽象的宠物店里有抽象的宠物, 它们都可以叫(.speak()). 具体到猫猫店
或者狗狗店, 从抽象宠物店生成即可.

                                   +--------------+
                                   |     Pet      |
 +---------------+                 | <<abstract>> |
 |    PetShop    |                 | +speak()     |
 | <<abstract>>  |                 | +__str__     |
 | +pet_factory  |                 +-+---------+--+
 | +buy_pet()    |                   |         |
 +-------------+-+           +-------+--+    +-+--------+
   |           |             |   Dog    |    |    Cat   |
   |           |             | +speak() |    | +speak() |
   |           |             | +__str__ |    | +__str__ |
   |           |             +------+---+    +--+----+--+
   |           |                    |           |    |
   |  +-----------------------------+-----------+    |
   |  |        |    +--------------------------------+
   |  |        |    |
+--+--+--+   +-+----+-+
|pet_shop|   |cat_shop|
+--------+   +--------+
 buy_pet()    buy_pet()


*抽象工厂模式应用场景?
[这些好难懂...]
- 一个系统不应当依赖于产品类实例如何被创建、组合和表达的细节，这对于所有形态
  的工厂模式都是重要的。
- 这个系统有多于一个的产品族，而系统只消费其中某一产品族，即同族的产品一起使用。
- 同属于同一个产品族的产品是在一起使用的，这一约束必须在系统的设计中体现出来。
- 系统提供一个产品类的库，所有的产品以同样的接口出现，从而使客户端不依赖于实现。

- 不同操作系统下, 都要有的 button, text 等
- QQ换皮肤, 一次一整套
- 同一品牌下的不同产品

*优缺点?
- 优点：当一个产品族中的多个对象被设计成一起工作时，它能保证客户端始终只使用同
  一个产品族中的对象。
- 缺点：产品族扩展非常困难，要增加一个系列的某一产品，既要在抽象的 Creator 里
  加代码，又要在具体的里面加代码。

*参考:
- https://www.github.com/faif/design-patterns
- https://www.runoob.com/design-pattern/abstract-factory-pattern.html
- https://blog.csdn.net/qq_33961117/article/details/90604014
- http://c.biancheng.net/view/1351.html

*概述:
    提供一组独立工厂的封装方式.
"""


import random
from typing import Type


class Pet:
    """抽象的宠物"""
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError


class Dog(Pet):
    """具体宠物:狗"""
    def speak(self) -> None:
        print("woof")

    def __str__(self) -> str:
        return f"Dog<{self.name}>"


class Cat(Pet):
    """具体宠物:猫"""
    def speak(self) -> None:
        print("meow")

    def __str__(self) -> str:
        return f"Cat<{self.name}>"


class PetShop:
    """抽象工厂类:宠物商店"""

    def __init__(self, animal_factory: Type[Pet]) -> None:
        """宠物工厂(pet_factory)是抽象工厂, 按自己需求填填."""
        self.pet_factory = animal_factory

    def buy_pet(self, name: str) -> Pet:
        """用抽象工厂创建及显示宠物"""
        pet = self.pet_factory(name)
        print(f"Here is your lovely {pet}")
        return pet


# Additional factories:

# Create a random animal 创建随机宠物
def random_animal(name: str) -> Pet:
    """随性点..."""
    return random.choice([Dog, Cat])(name)


# Show pets with various factories 宠物工厂开工
def main() -> None:
    """
    # 猫猫店的实例, 只卖猫, 然后买一只,叫 Lucy
    >>> cat_shop = PetShop(Cat)
    >>> pet = cat_shop.buy_pet("Lucy")
    Here is your lovely Cat<Lucy>
    >>> pet.speak()
    meow

    # 卖某种宠物的店, 随机叫什么, 是猫是狗也随机
    >>> shop = PetShop(random_animal)
    >>> for name in ["Max", "Jack", "Buddy"]:
    ...    pet = shop.buy_pet(name)
    ...    pet.speak()
    ...    print("=" * 20)
    Here is your lovely Cat<Max>
    meow
    ====================
    Here is your lovely Dog<Jack>
    woof
    ====================
    Here is your lovely Dog<Buddy>
    woof
    ====================
    """


if __name__ == "__main__":
    random.seed(1234)  # for deterministic doctest outputs
    import doctest

    doctest.testmod()
