#!/usr/local/bin/python3
"""
*对象池模式做什么用的?
如果经常需要创建一些对象即费时费力, 可是又很常用, 一次又只用不多的几个, 那对象池
就很合适. 池中的实例可被缓存, 被管理. 如果池中有可用实例, 就有机会跳过特别耗时耗
资源创建阶段. 从对象池中可以选出 (check out) 未用的对象, 并返给用户. 如果池中
没有可用对象, 就立即创建一个.

*本例做什么了?
本例用了队列 queue.Queue 来创建对象池(用 with 语句包裹的自定义对象池), 结果用
字符串填充.
第一个字符串对象输入 "yam", 用了 with 语句, with 块结束后, 释放回池中, 再次
sample_queue.get() 会重复使用刚才那个对象.
当删除(由GC)函数中创建的ObjectPool并返回对象时，对于“sam”也会发生同样的事情。

*对象池哪里用得到?

*参考:
https://github.com/faif/python_patterns

*概述 TL;DR
保存一组初始化好的实例对象, 以供开箱即用.
"""


class ObjectPool:
    """带 with 功能的队列管理"""

    def __init__(self, queue, auto_get=True) -> None:
        self._queue = queue
        self.item = self._queue.get() if auto_get else None

    def __enter__(self):
        """如果 item 为空, 从队列取出一个"""
        if self.item is None:
            self.item = self._queue.get()
        return self.item

    def __exit__(self, exc_type, exc_value, traceback):
        """如果 item 不空, 把 item 存入队列后, 设为 None"""
        if self.item is not None:
            self._queue.put(self.item)
            self.item = None

    def __del__(self):
        """GC 的时候存一下"""
        if self.item is not None:
            self._queue.put(self.item)
            self.item = None


def main():
    """
    >>> import queue

    >>> def test_object(queue):
    ...     pool = ObjectPool(queue, True)
    ...     print(f'Inside func: {pool.item}')

    >>> sample_queue = queue.Queue()

    # 例一, 用 with 包裹的对象池, with 之后对象扔在队列里
    >>> sample_queue.put('yam')
    >>> with ObjectPool(sample_queue) as obj:
    ...     print(f'Inside with: {obj}')
    Inside with: yam

    # 队列 get 之后可就没了啊
    >>> print(f'Outside with: {sample_queue.get()}')
    Outside with: yam

    # 例二, 在函数里直接使用 ObjectPool 对象池
    >>> sample_queue.put('sam')
    >>> test_object(sample_queue)
    Inside func: sam

    # 队列里 get 出来 (get后就空了)
    >>> print(f'Outside func: {sample_queue.get()}')
    Outside func: sam

    # 池子里加入多个对象, 注意这时候的顺序! hmm, 这里有点怪, 暂不理解.
    >>> sample_queue.put('yaya')
    >>> sample_queue.put('mimo')
    >>> while not sample_queue.empty():
    ...     test_object(sample_queue)
    ...     print(sample_queue.get())
    Inside func: yaya
    mimo
    Inside func: yaya
    yaya


    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
