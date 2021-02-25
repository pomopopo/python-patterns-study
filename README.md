# python 设计模式学习

> 主要资料源自 faif/python-patterns，后续补充其他一些地方来的资料。

这是一个 `python` `设计模式`及用法的汇总.

## 现有的模式

### 创建型模式 Creational Patterns
| 模式 | 描述 |
|:---:|------|
| [factory 工厂](patterns/factory.py) | **委托**某特定的函数/方法去创建新实例 |
| [abstract factory 抽象工厂](patterns/abstract_factory.py) | 对特定工厂使用通用函数(泛型) |
| [singleton 单例模式](patterns/singleton.py) | 只会有一个类实例(似乎拆成多个比较好) |
| [borg 单例共享](patterns/borg.py) | 在实例间共享单例的 **状态** |
| [builder 创建者](patterns/builder.py) | 创建者通过接收不同参数, 返回不同的对象. 构造函数就一个, 无需多个. |
| lazy evaluation 懒评价 | 延迟表达式的评估 |
| pool 对象池 | 预先创建并维护 **一组同类型的** 实例 |
| prototype 原型 | 因为生成实例的代价很大, 所以新实例就应该用原型的工厂和克隆来创建 |


### 结构型模式 Structural Patterns
| 模式 | 描述 |
|:---:|------|
| 3层 | 数据--业务逻辑--呈现,三层分离(严格关系) |
| 适配器 | 用**白名单**,把一个接口适配成另一个 |
| 桥接 | 通过中间人减少接口变化的影响 |
| 合成 |  |
| 装饰器 |  |
| 轻量 | 透明地**重用**具有相似/同**状态**的对象实例 |
| ? |  |
| MVC | 模型--视图--控制(非严格关系) |
| 代理 |  |


### 行为型模式 Behavioral Patterns
| 模式 | 描述 |
|:---:|------|
| 责任链 |  |
| 目录 |  |
| 链式调用 |  |
| 命令 |  |
| 迭代器 |  |
| 迭代器2 |  |
| 中介 |  |
| memento |  |
| 观察者 |  |
| 发布/订阅 |  |
| 注册 |  |
| specification |  |
| 状态 |  |
| 策略 |  |
| 模板 |  |
| 访问者 |  |

### ?

### 其他


## 一些基础知识

### 设计模式的6个基本原则
- 开闭原则 OCP: 对扩展开放, 对修改关闭.
- 里氏替换原则 LSP: 继承复用的基石. 子类可以替代基类出现. 反之不能.(lsp和多态的区别: lsp子类可以替换父类, 但是多态的子类实现可能完全不同,只是名字一样,就不能替换父类. --TronjanDonkey)
- 依赖倒转原则 DIP: 依赖抽象, 不要依赖具体.
- 接口隔离原则 ISP: 多个隔离的接口, 优于单个接口.
- 最少知道原则 DP: 一个实体尽量少于其他实体相互作用, 尽量独立.
- 合成复用原则 CRP: 合成/聚合, 优于继承.


### 什么时候用设计模式?
- 要有点语法基础, 至少语法学个七七八八
- 有点面向对象的基础, 有些 OO 的概念
- 写不是特别小的东西, 可能要分模块的那种

### 为什么用设计模式?
- 模式是前人项目经验的总结, 利于他人理解, 可靠性高
- 让程序更适应变化
- 模块/写过的东西, 更容易复用, 减少反复造轮子

### 当心误区
- 要避免过度设计
- ?


