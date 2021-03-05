#!/usr/local/bin/python3
"""
*来源
http://code.activestate.com/recipes/131499-observer-pattern/

*本例

*应用场景
Django 信号处理: https://docs.djangoproject.com/en/3.1/topics/signals/
flask 信号处理: https://flask.palletsprojects.com/en/1.1.x/signals/

*概述
维护依赖列表, 遇到状态变化时, 按列表通知.
"""


class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self) -> None:
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)


class Data(Subject):
    def __init__(self, name=''):
        super().__init__()
        self.name = name
        self._data = 0

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.notify()


class HexViewer:
    def update(self, subject):
        print(
            f'HexViewer: subject `{subject.name}` has data `0x{subject.data:X}`')


class DecimalViewer:
    def update(self, subject):
        print(
            f'DecimalViewer: subject `{subject.name}` has data `{subject.data}`')


def main():
    data1 = Data('Data_1')
    data2 = Data('Data_2')
    view1 = HexViewer()
    view2 = DecimalViewer()

    data1.attach(view1)
    data1.attach(view2)

    data1.data = 10
    data1.data = 3
    data1.detach(view2)
    data1.data = 10

    data2.attach(view2)
    data2.attach(view1)
    data2.data = 15
    data2.data = 5
    data2.detach(view1)
    data2.data = 15


def test():
    """
    >>> d1 = Data('Data_1')
    >>> d2 = Data('Data_2')
    >>> v1 = HexViewer()
    >>> v2 = DecimalViewer()

    # 添加两个观察者
    >>> d1.attach(v1)
    >>> d1.attach(v2)

    # 更改数据就会有通知
    >>> d1.data = 10
    HexViewer: subject `Data_1` has data `0xA`
    DecimalViewer: subject `Data_1` has data `10`

    # 更改数据就会有通知
    >>> d1.data = 3
    HexViewer: subject `Data_1` has data `0x3`
    DecimalViewer: subject `Data_1` has data `3`

    # 被取消通知的对象, 就不会再接收到
    >>> d1.detach(v2)
    >>> d1.data = 10
    HexViewer: subject `Data_1` has data `0xA`

    # 添加顺序影响通知顺序
    >>> d2.attach(v2)
    >>> d2.attach(v1)
    >>> d2.data = 15
    DecimalViewer: subject `Data_2` has data `15`
    HexViewer: subject `Data_2` has data `0xF`

    # 更改数据就会有通知
    >>> d2.data = 5
    DecimalViewer: subject `Data_2` has data `5`
    HexViewer: subject `Data_2` has data `0x5`

    # 被取消通知的对象, 就不会再接收到
    >>> d2.detach(v1)
    >>> d2.data = 15
    DecimalViewer: subject `Data_2` has data `15`
    """


if __name__ == "__main__":
    main()
    import doctest
    doctest.testmod()
