#!/usr/local/bin/python3
"""
*什么是桥接?
把类的 *功能* 层次结构和 *实现* 层次结构分离.

*桥接模式目的
桥接涉及到桥接的接口, 使得实体类(implement)的功能独立于接口实现类.
两种类型的类内部变化, 各自互不影响.

基于类的最小设计原则

*本例?
画圆圈的类(CircleShape)在实例化的时候,可以指定使用 DrawingAPI_1
或者 DrawingAPI_2 哪个 api, 调用的时候, 就能使用其具体功能.

                        +----------------+
                        |  DrawingAPI_1  | 实体类
    抽象类               +----------------+
+------------+      +---- + draw_circle()|
| DrawShape  |      |   +----------------+
+------------+      |
| + draw() <---intf-+   +----------------+
| + scale()  |      |   |  DrawingAPI_2  | 实体类
+------------+      |   +----------------+
                    +---- + draw_circle()|
                        +----------------+

*优缺点
- 优点:
    1 可以替代多层继承, 减少子类个数, 降低维护难度.
    2 抽象和实现分离
    3 扩展能力优秀
    4 实现细节对客户透明.
- 缺点:
    1 增加系统的理解和设计难度; 聚合和关联建立在抽象层, 开发要针对抽象层设计.
    2 要能正确识别系统两个独立变化的维度, 适用范围有些受限.

*使用场景
- jdbc 驱动
- 银行转账系统: 转账分类(网银/柜台/atm), 用户类型(普通用户/银行卡/金卡)
- OA消息管理: 消息类型(及时/延时), 消息分类(手机/邮件/qq)
- HR的奖金: 奖金分类(个人/团队/激励), 部门分类(人事/销售/研发)

*和工厂的异同?
- 工厂: 创建对象                    自己提出,但交给厂家生产
- 桥接: 将抽象的不同形式与具体实现分离  自己的产品调用某个对象的某个方法

*参考
https://github.com/faif/python_patterns
https://blog.csdn.net/aHardDreamer/article/details/89463662

*概述
把实现和抽象解耦.
"""


class DrawingAPI_1:
    """实现类, 1/2, 完成具体画圆工作"""

    def draw_circle(self, x, y, radius):
        print(f'API_1.circle at {x}.{y} r = {radius}')


class DrawingAPI_2:
    """实现类, 2/2, 完成另一种具体画圆工作"""

    def draw_circle(self, x, y, radius):
        print(f'API_2.circle at {x}.{y} r = {radius}')


class CircleShape:
    """抽象类, 具体画图工作不由自己完成"""

    def __init__(self, x, y, radius, drawing_api):
        self._x = x
        self._y = y
        self._radius = radius
        self._drawing_api = drawing_api

    # 低阶操作, 指定实现方式
    def draw(self):
        self._drawing_api.draw_circle(self._x, self._y, self._radius)

    # 高价操作, 抽象相关, 不涉及具体 api
    def scale(self, pct):
        self._radius *= pct


def test():
    shapes = (
        CircleShape(1, 2, 3, DrawingAPI_1()),
        CircleShape(5, 7, 9, DrawingAPI_2())
    )

    # print(shapes)
    for shape in shapes:
        shape.draw()
        shape.scale(2.5)
        shape.draw()
        print('-'*4)


def main():
    """
    >>> shapes = (
    ...     CircleShape(1,2,3,DrawingAPI_1()),
    ...     CircleShape(5,7,9,DrawingAPI_2())
    ... )

    >>> for shape in shapes:
    ...     shape.draw()
    ...     shape.scale(2.5)
    ...     shape.draw()
    ...     print('-'*4)
    API_1.circle at 1.2 r = 3
    API_1.circle at 1.2 r = 7.5
    ----
    API_2.circle at 5.7 r = 9
    API_2.circle at 5.7 r = 22.5
    ----
    """


if __name__ == "__main__":
    # test()

    import doctest
    doctest.testmod(verbose=True)
