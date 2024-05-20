#### 1.参考教材6.2，结合项目的进程和开发历程，从设计原则的几个方面，组员对负责设计的模块进行评估，思考存在的问题和解决方案。

##### （1）模块化：

我们将项目划分为了用户模块、商品模块、店铺模块、评论模块，将各不相关的部分进行了隔离，较好地实现了关注点分离。每个模块都有自己唯一目的，并且相对独立于其他模块。

但对于各个模块的代码可能存在相互调用的情况，可以对代码进一步优化。

##### （2）接口：

我们在项目中设计的接口封装和隐藏了软件单元的设计和实现细节，并且满足单一职责原则 (Single Responsibility Principle, SRP)，每个模块和接口只负责一项职责，这样可以使系统更易于理解、维护和扩展；满足接口隔离原则 (Interface Segregation Principle, ISP)，即接口小而专，避免了臃肿。

##### （3）信息隐藏：

在信息隐藏方面，我们对敏感信息进行了封装，通过限制对类或模块内部数据的直接访问，保护其不被外部代码意外修改。

##### （4）增量式开发：

我们的项目采用模块化设计，各个模块相对独立，可以独立开发、测试和部署；模块设计时考虑到未来的扩展性，使得在后续迭代中可以方便地添加新功能，满足增量式开发的基本要求。

##### （5）抽象：

我们的线上商城项目抽象出了不同层次的功能，封装了一些基础函数，如获取获取用户基本信息等函数，使高层模块不依赖于低层模块的实现细节，而是通过抽象接口进行交互。

##### （6）通用性：

我们在设计项目的功能时将特定的上下文环境信息参数化，并且去除了前置条件，简化了后置条件，大大提升了各个模块的通用性。

#### 2.阅读下面DI资料（或查阅其它相关资料），学习依赖注入技术（Dependency Injection-A Practical Introduction.pdf）

依赖注入（Dependency Injection，简称 DI）是一种软件设计模式，用于实现控制反转（Inversion of Control，简称 IoC）。在这种模式中，依赖关系通过外部注入到一个对象中，而不是由对象自身创建和管理。这种设计使得代码更加模块化、可测试和可维护。

可以通过构造函数注入：

```python
class Service:
    def __init__(self, repository):
        self.repository = repository

repo = Repository()
service = Service(repo)

```

也可以通过属性注入：

```python
class Service:
    def set_repository(self, repository):
        self.repository = repository

repo = Repository()
service = Service()
service.set_repository(repo)

```

