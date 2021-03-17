#!/usr/local/bin/python3
"""
*本例
本例实现了一个有消息中心的电视台, 有的节目有人订阅, 有的没人订. 不过没关系,
不管订不订阅, 电视台都保持播出(发布). 订阅了的节目, 也可以取消.
消息中心更新后, 消息队列就清空.

+------------------+  message_center +----------------+     ffTV +-------------+
| Subscriber       +---------------->+ Provider       +<---------+ Publisher   |
+------------------+                 +----------------+          +-------------+
| subscribe()   o  |                 | notify()    o <------------- publish()  |
| unsubscribe() ^  |                 | subscribe()    |          +-------------+
| run()         |  |                 | unsubscribe()  |
+------------------+                 | update()    o  |
                |                    +-------------^--+
+---------------+------+                           |
| ConcreteSubscriber 1 +---+                       |
+---------------------+ 2 +---+     +-------------+-----------+
    +----------------------+ n |     | message_center.update() |
        +----------------------+     +-------------------------+


*大内参
http://www.slideshare.net/ishraqabd/publish-subscribe-model-overview-13368808
Author: https://github.com/HanWenfan

"""


class Provider:
    def __init__(self):
        self.msg_queue = []
        self.subscribers = {}

    def notify(self, msg):
        self.msg_queue.append(msg)

    def subscribe(self, msg, subscriber):
        self.subscribers.setdefault(msg, []).append(subscriber)

    def unsubscribe(self, msg, subscriber):
        self.subscribers[msg].remove(subscriber)

    def update(self):
        for msg in self.msg_queue:
            for sub in self.subscribers.get(msg, []):
                sub.run(msg)
        self.msg_queue = []


class Publisher:
    def __init__(self, msg_center):
        self.provider = msg_center

    def publish(self, msg):
        self.provider.notify(msg)


class Subscriber:
    def __init__(self, name, msg_center):
        self.name = name
        self.provider = msg_center

    def subscribe(self, msg):
        self.provider.subscribe(msg, self)

    def unsubscribe(self, msg):
        self.provider.unsubscribe(msg, self)

    def run(self, msg):
        print(f'{self.name} got {msg}')


def main():
    """
    >>> message_center = Provider()
    >>> fftv = Publisher(message_center)

    >>> eden = Subscriber('Eden', message_center)
    >>> eden.subscribe('cartoon')
    >>> eden.subscribe('movie')
    >>> eden.unsubscribe('movie')

    >>> jack = Subscriber('Jack', message_center)
    >>> jack.subscribe('music')

    >>> hebe = Subscriber('Hebe', message_center)
    >>> hebe.subscribe('movie')

    >>> alex = Subscriber('Alex', message_center)
    >>> alex.subscribe('music')
    >>> alex.unsubscribe('music')

    # 1 没人订阅广告 `ads`
    # 2 eden 改了一次订阅内容

    >>> fftv.publish('cartoon')
    >>> fftv.publish('music')
    >>> fftv.publish('ads')
    >>> fftv.publish('movie')
    >>> fftv.publish('blank')
    >>> fftv.publish('movie') # 又发布了一次 movie 节目
    >>> # fftv.publish('cartoon')

    >>> message_center.update()
    Eden got cartoon
    Jack got music
    Hebe got movie
    Hebe got movie
"""

if __name__ == "__main__":
    # main()
    import doctest
    doctest.testmod(verbose=True)
