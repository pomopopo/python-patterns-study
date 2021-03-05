#!/usr/local/bin/python3
"""
*代理是撒子嘛
对一个现存类既想增加接口, 又不想修改自身代码, 那就用代理好了. 主类叫
真正主体(Real Subject), 客户端通过代理或直接访问真正主体时, 无需改
变任何代码, 所以上述二者之间必须有相同的接口.

*本例?
本例的真实主体是能正常工作的, 代理加了授权和日志两个功能. client 构造成
可以指定用代理还是真实主体, 方便灵活使用.

类的结构关系
+--------+                   +-----------------+
| client +------------------^+     Subject     |
+--------+                   |  <<interface>>  |
                             +-----------------+
                             | do_the_job()    |
                             +--------+--------+
                                      ^
      +-------------------------------+
      |                               |
+-----+------+  real_subject +--------+--------+
|RealSubject +<--------------+      Proxy      |
+------------+               +-----------------+
|do_the_job()|               | do_the_job() o------- real_subject.do_the_job()
+------------+               +-----------------+

运行的调用过程
+----------+
|  client  |        +---------------+
+----------+        |    proxy      |       +------------+
|subject *--------->+---------------+       |real_subject|
+----------+        |real_subject *-------->+------------+
                    +---------------+       |            |
                                            +------------+

*哪里耍嘞?
- 日志或者入口控制, 需要访问真实主题, 用之.
- 用代理服务器连接出网
- 销售代理(厂商)
- 律师代理(客户)
- Foxmail
- 枪手

*参考
https://github.com/faif/python_patterns
https://blog.csdn.net/longronglin/article/details/1454315

*一言以蔽之
不改原接口, 增加功能或逻辑(如日志/缓存/认证等)
"""


class Subject:
    '''为保证接口一致而建, 非必须, 但建议有'''

    def do_the_job(self, user: str) -> None:
        raise NotImplementedError


class RealSubject(Subject):
    '''干活的! 支付网关这类外部服务就是个好例子'''

    def do_the_job(self, user: str) -> None:
        print(f'`{user}` is doing the job.')


class Proxy(Subject):
    def __init__(self) -> None:
        self._real_subject = RealSubject()

    def do_the_job(self, user: str) -> None:
        '''增加了日志和权限功能'''
        print(f'[LOG] doing job for `{user}` is requested.')

        if user == 'admin':
            self._real_subject.do_the_job(user)
        else:
            print('[LOG] only `admin` has the priority.')


def client(job_doer, user):
    job_doer.do_the_job(user)


def test():
    proxy = Proxy()
    real_subject = RealSubject()

    client(proxy, 'admin')
    client(proxy, 'anonymouse')

    client(real_subject, 'admin')
    client(real_subject, 'anonymouse')


def main():
    """
    >>> proxy = Proxy()
    >>> real_subject = RealSubject()

    >>> client(proxy, 'admin')
    [LOG] doing job for `admin` is requested.
    `admin` is doing the job.

    >>> client(proxy, 'anonymouse')
    [LOG] doing job for `anonymouse` is requested.
    [LOG] only `admin` has the priority.

    >>> client(real_subject, 'admin')
    `admin` is doing the job.

    >>> client(real_subject, 'anonymouse')
    `anonymouse` is doing the job.
    """


if __name__ == "__main__":

    import doctest
    doctest.testmod(verbose=True)

    test()
