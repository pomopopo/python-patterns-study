# python 设计模式学习

> 主要资料源自 faif/python-patterns，后续补充其他一些地方来的资料。

这是一个 `python` `设计模式`及用法的汇总.

## 现有的模式

### 创造模式 Creational Patterns
| 模式 | 描述 |
|:---:|------|
| factory 工厂 | 委托某特定的函数/方法去创建实例 |
| [abs factory 抽象工厂](patterns/abstract_factory.py) | 对特定工厂使用通用函数(泛型) |
| [borg 单例共享](patterns/borg.py) | 在实例间共享单例的 **状态** |
| builder 建造者 | 建造者通过接收不同参数, 返回不同的对象. 构造函数就一个, 无需多个. |
| lazy evaluation 懒评价 | 延迟表达式的评估 |
| pool 对象池 | 预先创建并维护 **一组同类型的** 实例 |
| prototype 原型 | 因为生成实例的代价很大, 所以新实例就应该用原型的工厂和克隆来创建 |


### 结构性模式 Structural Patterns


### 行为模式 Behavioral Patterns


### 其他