#!/usr/local/bin/python3
"""
*是什么
适配器模式为类提供一个不同的接口. 可以类比成手机充电器, 用在不同插座上的转换头.
按照这个思路, 适配器模式可以用来集成原本不兼容接口, 转成兼容类型.

*本例做了什么
斯有实体(狗, 猫, 人, 车), 各鸣其声. 适配器类对各自原始出声方法提供不同接口, 故
原接口(吠, 喵)在共同 make_noise() 名下可用.

*哪里用
- Grok 框架, 用来适配 API.
http://grok.zope.org/doc/current/grok_overview.html#adapters

*为什么


*参考谁
https://github.com/faif/python_patterns

*概述
允许一个既有类的接口可以被另一个接口使用.
"""

# 一些有各自接口的不同类


class Dog:
    def __init__(self):
        self.name = 'Dog'

    def bark(self):
        return 'woof!'


class Cat:
    def __init__(self):
        self.name = 'Cat'

    def meow(self):
        return 'meow!'


class Human:
    def __init__(self):
        self.name = 'Human'

    def speak(self):
        return 'Hello?'


class Car:
    def __init__(self):
        self.name = 'Car'

    def beep(self, octane_level=1):
        return f'vroom{"!"*octane_level}'


# 适配器
class Adapter:
    def __init__(self, obj, **adapted_methods):
        '''把 adapted_methods 存到 __dict__ '''
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __getattr__(self, attr):
        '''没指定适配关系的, 就传回到原类里'''
        return getattr(self.obj, attr)

    def original_dict(self):
        return self.obj.__dict__


def main():
    """
    <__main__.Dog object at 0x10f73cf70>
    {'name': 'Dog'}
    [<__main__.Adapter object at 0x10f778550>]
    <__main__.Dog object at 0x10f73cf70> <bound method Dog.bark of <__main__.Dog object at 0x10f73cf70>>
    {'name': 'Dog'}
    A "Dog" goes "woof!"
    A "Cat" goes "meow!"
    A "Human" goes "Hello?"
    A "Car" goes "vroom!!!"
    """
    objs = []
    dog = Dog()
    print(dog)
    print(dog.__dict__)

    objs.append(Adapter(dog, make_noise=dog.bark))
    print(objs)
    print(objs[0].__dict__['obj'], objs[0].__dict__['make_noise'])
    print(objs[0].original_dict())

    cat = Cat()
    objs.append(Adapter(cat, make_noise=cat.meow))
    man = Human()
    objs.append(Adapter(man, make_noise=man.speak))
    car = Car()
    objs.append(Adapter(car, make_noise=lambda: car.beep(3)))

    for item in objs:
        print(f'A "{item.name}" goes "{item.make_noise()}"')


def test():
    cat = Cat()
    cat_adp = Adapter(cat, make_noise=cat.meow)
    print(cat_adp.make_noise())


if __name__ == "__main__":
    # test()
    main()

    import doctest
    doctest.testmod()
