#!/usr/local/bin/python3
"""
*干啥的?
黑板模式中, 数个专门子系统(知识源)组织其知识, 构建成一个部分或可能的解决方案.
这样, 子系统们一起工作处理问题, 解决方案就是各部分的总和.


"""

import abc
import random


class Blackboard:
    def __init__(self) -> None:
        self.experts = []
        self.common_state = {
            'problems': 0,
            'suggestions': 0,
            'contributions': [],
            'progress': 0,
        }

    def add_expert(self, expert):
        self.experts.append(expert)


class Controller:
    def __init__(self, blackboard):
        self.blackboard = blackboard

    def run_loop(self):
        while self.blackboard.common_state['progress'] < 100:
            for expert in self.blackboard.experts:
                if expert.is_eager_to_contribute:
                    expert.contribute()
        return self.blackboard.common_state['contributions']


class AbstractExpert(metaclass=abc.ABCMeta):
    def __init__(self, blackboard):
        self.blackboard = blackboard

    @property
    @abc.abstractmethod
    def is_eager_to_contribute(self):
        raise NotImplementedError('must provide impl in sub class')

    @abc.abstractmethod
    def contribute(self):
        raise NotImplementedError('must provide impl in sub class')


class Student(AbstractExpert):
    @property
    def is_eager_to_contribute(self):
        return True

    def contribute(self):
        self.blackboard.common_state['problems'] += random.randint(1, 10)
        self.blackboard.common_state['suggestions'] += random.randint(1, 10)
        self.blackboard.common_state['contributions'] += [
            self.__class__.__name__]
        self.blackboard.common_state['progress'] += random.randint(1, 2)


class Scientist(AbstractExpert):
    @property
    def is_eager_to_contribute(self):
        return random.randint(0, 1) == 1

    def contribute(self):
        self.blackboard.common_state['problems'] += random.randint(10, 20)
        self.blackboard.common_state['suggestions'] += random.randint(10, 20)
        self.blackboard.common_state['contributions'] += [
            self.__class__.__name__]
        self.blackboard.common_state['progress'] += random.randint(10, 30)


class Professor(AbstractExpert):
    @property
    def is_eager_to_contribute(self):
        return self.blackboard.common_state['problems'] > 100

    def contribute(self):
        self.blackboard.common_state['problems'] += random.randint(1, 2)
        self.blackboard.common_state['suggestions'] += random.randint(10, 20)
        self.blackboard.common_state['contributions'] += [
            self.__class__.__name__]
        self.blackboard.common_state['progress'] += random.randint(10, 100)



def main():
    """
    >>> random.seed(12)

    >>> blackboard = Blackboard()
    >>> blackboard.add_expert(Student(blackboard))
    >>> blackboard.add_expert(Scientist(blackboard))
    >>> blackboard.add_expert(Professor(blackboard))

    >>> c = Controller(blackboard)
    >>> contrib = c.run_loop()

    >>> from pprint import pprint
    >>> pprint(contrib)
    ['Student',
     'Student',
     'Scientist',
     'Student',
     'Student',
     'Scientist',
     'Student',
     'Scientist',
     'Student',
     'Scientist',
     'Professor']
    """


if __name__ == "__main__":
    # main()

    import doctest
    doctest.testmod(verbose=True)