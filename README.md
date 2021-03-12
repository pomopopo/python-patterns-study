# python 设计模式学习

这是一个 `python` `设计模式` 及其用法的汇总. 主要资料源自 faif/python-patterns.

## 现有的模式

按常用程度, 标记为 🥇 🥈 🥉.

### 创建型模式 Creational Patterns
| 模式                                                      | 描述                                                                |
| --------------------------------------------------------- | ------------------------------------------------------------------- |
| [factory 工厂](patterns/factory.py)                       | 🥈 **委托**某特定的函数/方法去创建新实例                             |
| [abstract factory 抽象工厂](patterns/abstract_factory.py) | 🥈 对特定工厂使用通用函数(泛型)                                      |
| [singleton 单例模式](patterns/singleton.py)               | 🥇 确保只有一个类实例, 并提供全局访问点(拆乎哉?)                     |
| [borg 单例共享](patterns/borg.py)                         | 在实例间共享单例的 **状态**                                         |
| [builder 创建者](patterns/builder.py)                     | 🥉 创建者通过接收不同参数, 返回不同的对象. 构造函数就一个, 无需多个. |
| [lazy evaluation 惰性求值](patterns/lazy_evaluation.py)   | 把类属性的计算求值推迟到调用时候(而不是类建立时候)                  |
| [pool 对象池](patterns/pool.py)                           | 预先创建并维护 **一组同类型的** 实例 (还有点不理解)                 |
| [prototype 原型](patterns/prototype.py)                   | 如果生成新实例的代价很大, 那么可以用工厂, 并且克隆原型来创建新实例  |


### 结构型模式 Structural Patterns
| 模式                                                        | 描述                                                                              |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [3-tier 3层](patterns/3-tier.py)                            | 数据--业务逻辑--呈现,三层分离(严格关系)                                           |
| [adapter 适配器](patterns/adapter.py)                       | 🥈 用**白名单**,把一个接口适配成另一个                                             |
| [bridge 桥接](patterns/bridge.py)                           | 🥉 通过中间人减少接口变化的影响                                                    |
| [composite 合成](patterns/composite.py)                     | 🥇 让客户端用同一个方式处理不同的对象/组合(部分--整体, 用树形结构组合)             |
| [decorator 装饰器](patterns/decorator.py)                   | 🥈 把功能包起来, 从而改变输出                                                      |
| [facade 门面/外观](patterns/facade.py)                      | 🥇 把一个类用作其他一些类的API, 是其他类高层接口, 使其他类更容易用(把零件组装电脑) |
| [flyweight 享元](patterns/flyweight.py)                     | 透明地**重用**具有相似/相同**状态**的对象实例                                     |
| [front controller 前端控制器](patterns/front_controller.py) | 到达应用的请求, 用单个程序处理?                                                    |
| MVC                                                         | 模型--视图--控制(非严格关系)                                                      |
| [proxy 代理](patterns/proxy.py)                             | 🥇 一个对象把另一个对象的操作控制起来,以代理控制对象访问                           |


### 行为型模式 Behavioral Patterns
| 模式                                                                 | 描述                                                |
| -------------------------------------------------------------------- | --------------------------------------------------- |
| [chain of resposibility 责任链](patterns/chain_of_responsibility.py) | 🥉 为数据处理提供一个链式可连续调用的句柄            |
| [catalog 目录](patterns/catalog.py)                                  | 根据创建类的参数, 由通用方法调用类内不同具体实现    |
| [chaining method 链式调用](patterns/chaining_method.py)              | 调用之后,可以继续调用自己的方法(用.连接)            |
| [command 命令](patterns/command.py)                                  | 🥈 **推迟绑定** 命令和参数 到调用上                  |
| [iterator 迭代器](patterns/iterator.py)                              | 🥇 提供一个容器, 通过容器能逐个访问内部对象          |
| [iterator2 迭代器2](patterns/iterator_alt.py)                        | 迭代器的 `__iter__` 实现                            |
| mediator 中介                                                        |                                                     |
| memento                                                              |                                                     |
| [observer 观察者](patterns/observer.py)                              | 🥇 当 **发生事件** 或 **数据变化**, 提供**回调**通知 |
| publish subscribe 发布/订阅                                          |                                                     |
| registry 注册                                                        |                                                     |
| specification                                                        |                                                     |
| state 状态                                                           | 🥈                                                   |
| stratory 策略                                                        | 🥈                                                   |
| [template 模板](patterns/template.py)                                | 🥇 一个对象定义了框架, 但其功能是可插入/替换的       |
| visitor 访问者                                                       |                                                     |

### 可测试模式的设计
| 模式                          | 描述              |
| ----------------------------- | ----------------- |
| dependency injection 依赖注入 | 3种依赖注入的方法 |

### 基础模式
| 模式                    | 描述                                     |
| ----------------------- | ---------------------------------------- |
| delegation pattern 委托 | 一个类把请求移交给另一个类处理(被委托人) |

### 其他
| 模式                | 描述                                                                     |
| ------------------- | ------------------------------------------------------------------------ |
| blackboard 黑板     | 结构模型, 将不同子系统的知识组建成解决方案, 是 AI 的解决方法, 非传统模式 |
| graph search 图搜索 | 图的算法, 非传统模式                                                     |
| HSM 层次状态机      | 层次状态机, 非传统模式                                                   |

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


## ref
- https://github.com/faif/python_patterns
- https://blog.csdn.net/longronglin/article/details/1454315