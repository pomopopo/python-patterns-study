#!/usr/local/bin/python3
"""
*什么是规约模式
经常用在 DDD 中, 用来将业务规则(通常是隐式业务规则)封装成独立的逻辑单元,
从而将隐式业务规则提炼为显示概念, 就能复用代码了.

隐式业务规则 vs 显示业务规则?
- 隐式规则
    if user.age < 18:
        raise Exception('too young')
- 显式规则
    adult = AdultSpecification() #这个要单独实现
    if not adult.is_satisfied_by(user):
        raise Exception('too young')

*为什么要用?
if判断太多, 不利于维护, 也不好说明意图.

*实现方法?
每个规约实现4个方法:is_satisfied_by(), and_specification(),
or_specification(), not_specification().

其中 is_satisfied_by() 实现业务规则, and or not 用来将业务复合在一起.

*本例?
本例创建了一个用户/超级用户规约, 用来判断具体的用户是不是超级用户.

                                                    +----------------+
                                                    | Specification  |
                                                    | << virtual >>  |
                                                    +-------+--------+
                                                            ^
            +----------------+                 +------------+-----------+
            |      User      +<>---------------+ CompositeSpecification |
            +-------+--------+                 +------------+-----------+
                    ^                                       ^
        +-----------+-----------+              +------------+-----------+
        |           |           |              |                        |
+-------+--+ +------+---+ +-----+----+ +-------+-----------+ +----------+-----------+
|   user   | |super_user| | not_user | | UserSpecification | |SuperUserSpecification|
+----------+ +----------+ +----------+ +-------------------+ +----------------------+
    andry        ivan        vasiliy

*应用场景?
- DDD
- 数据查询: 筛选条件

*参考
https://www.cnblogs.com/youring2/p/Specification-Pattern.html

*概要
用布尔逻辑链式重组业务逻辑
"""

from abc import abstractclassmethod


class Specification:
    def and_specification(self, candidate):
        raise NotImplementedError()

    def or_specification(self, candidate):
        raise NotImplementedError()

    def not_specification(self):
        raise NotImplementedError()

    @abstractclassmethod
    def is_satisfied_by(self, candidate):
        pass


class CompositeSpecification(Specification):
    @abstractclassmethod
    def is_satisfied_by(self, candidate):
        pass

    def and_specification(self, candidate):
        return AndSpecification(self, candidate)

    def or_specification(self, candidate):
        return OrSpecification(self, candidate)

    def not_specification(self):
        return NotSpecification(self)


class AndSpecification(CompositeSpecification):
    _one = Specification()
    _other = Specification()

    def __init__(self, one, other) -> None:
        self._one = one
        self._other = other

    def is_satisfied_by(self, candidate):
        return bool(
            self._one.is_satisfied_by(candidate)
            and self._other.is_satisfied_by(candidate)
        )


class OrSpecification(CompositeSpecification):
    _one = Specification()
    _other = Specification()

    def __init__(self, one, other) -> None:
        self._one = one
        self._other = other

    def is_satisfied_by(self, candidate):
        return bool(
            self._one.is_satisfied_by(candidate)
            or self._other.is_satisfied_by(candidate)
        )


class NotSpecification(CompositeSpecification):
    _wrapped = Specification()

    def __init__(self, wrapped):
        self._wrapped = wrapped

    def is_satisfied_by(self, candidate):
        return bool(not self._wrapped.is_satisfied_by(candidate))


class User:
    def __init__(self, super_user=False) -> None:
        self.super_user = super_user


class UserSpecification(CompositeSpecification):
    def is_satisfied_by(self, candidate):
        return isinstance(candidate, User)


class SuperUserSpeicification(CompositeSpecification):
    def is_satisfied_by(self, candidate):
        return getattr(candidate, 'super_user', False)


def main():
    andry = User()
    ivan = User(super_user=True)
    vasiliy = 'not user instance'

    root_spec = UserSpecification().and_specification(SuperUserSpeicification())

    print(root_spec.is_satisfied_by(andry))     # False
    print(root_spec.is_satisfied_by(ivan))      # True
    print(root_spec.is_satisfied_by(vasiliy))   # False


if __name__ == "__main__":
    main()
