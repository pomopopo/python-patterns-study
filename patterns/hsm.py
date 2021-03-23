#!/usr/local/bin/python3
"""
*状态机的三生三世
- FSM 有限状态机. 根据输入条件不同, 系统在不同状态间跳转. 可以通过状态(转移)图或
状态转移表实现. 因为图比较直观, 用图的人比较多.
实现方式可以是 if ... else 或者 switch ... case 也可以是 GoF 的 状态模式.

- HSM 层次状态机. 各层之间可以用嵌套概念, 大部分事件由最上层处理, 程序只需要注册
少数感兴趣的事件响应(如点击按钮). 这种事件向父层传递, 子层继承了父类行为, 这种包含
嵌套的状态机, 称为 HSM 层次状态机.

- FSM vs HSM.
    - 结构上: FSM 的状态之间相互独立, 状态图没有的部分, 状态机是平坦的; 实际模型
通常 FSM 不适用, 问题本身会有域或者值的嵌套, HSM 状态更灵活, 可以有嵌套.
    - 维护上: 对 FSM 来说, 状态多了之后, 跳转太多, 容易变得不可维护, 而且很难知道
为什么自己在这个状态里. HSM 的话, 行为分类了, 几个小状态归并到一个状态里, 分层跳转.


"""


class UnsupportedMessageType(BaseException):
    pass


class UnsupportedState(BaseException):
    pass


class UnsupportedTransition(BaseException):
    pass


class HierachicalStateMachine:
    def __init__(self):
        self._active_state = Active(self)
        self._standby_state = Standby(self)
        self._suspect_state = Suspect(self)
        self._failed_state = Failed(self)
        self._current_state = self._standby_state
        self.states = {
            'active': self._active_state,
            'standby': self._standby_state,
            'suspect': self._suspect_state,
            'failed': self._failed_state,
        }
        self.message_types = {
            'fault trigger': self._current_state.on_fault_trigger,
            'switchover': self._current_state.on_switchover,
            'diagnostics passed': self._current_state.on_diagnostics_passed,
            'diagnostics failed': self._current_state.on_diagnostics_fialed,
            'operator inservice': self._current_state.on_operator_inservice,
        }

    def _next_state(self, state):
        try:
            self._current_state = self.states[state]
        except KeyError:
            raise UnsupportedState

    def _send_diagnostics_request(self):
        return 'send diagnostic request'

    def _raise_alarm(self):
        return 'raise alarm'

    def _clear_alarm(self):
        return 'clear alarm'

    def _perform_switchover(self):
        return 'perform switchover'

    def _send_switchover_response(self):
        return 'send switchover response'

    def _send_operator_inservice_response(self):
        return 'send operator inservice response'

    def _send_diagnostics_failure_report(self):
        return 'send diagnostics failure report'

    def _send_diagnostices_pass_report(self):
        return 'send diagnostics pass report'

    def _abort_diagnositcs(self):
        return 'abort diagnostics'

    def _check_mate_status(self):
        return 'check mate status'

    def on_message(self, message_type):
        if message_type in self.message_types.keys():
            self.message_types[message_type]()
        else:
            raise UnsupportedMessageType


class Unit:
    def __init__(self, HierachicalStateMachine):
        self.hsm = HierachicalStateMachine

    def on_switchover(self):
        raise UnsupportedTransition

    def on_fault_trigger(self):
        raise UnsupportedTransition

    def on_diagnostics_fialed(self):
        raise UnsupportedTransition

    def on_diagnostics_passed(self):
        raise UnsupportedTransition

    def on_operator_inservice(self):
        raise UnsupportedTransition


class Inservice(Unit):
    def __init__(self, HierachicalStateMachine):
        self._hsm = HierachicalStateMachine

    def on_fault_trigger(self):
        self._hsm._next_state('suspect')
        self._hsm._send_diagnostics_request()
        self._hsm._raise_alarm()

    def on_switchover(self):
        self._hsm._perform_switchover()
        self._hsm._check_mate_status()
        self._hsm._send_switchover_response()


class Active(Inservice):
    def __init__(self, HierachicalStateMachine):
        self._hsm = HierachicalStateMachine

    def on_fault_trigger(self):
        super().perform_switchover()  # ?
        super().on_fault_trigger()

    def on_switchover(self):
        self._hsm.on_switchover()
        self._hsm.next_state('standby')


class Standby(Inservice):
    def __init__(self, HierachicalStateMachine):
        self._hsm = HierachicalStateMachine

    def on_switchover(self):
        super().on_switchover()
        self._hsm._next_state('active')


class OutOfService(Unit):
    def __init__(self, HierachicalStateMachine):
        self._hsm = HierachicalStateMachine

    def on_operator_inservice(self):
        self._hsm.on_switchover()
        self._hsm.send_operator_inservice_response()
        self._hsm.next_state('suspect')


class Suspect(OutOfService):
    def __init__(self, HierachicalStateMachine):
        self._hsm = HierachicalStateMachine

    def on_diagnostics_fialed(self):
        super().send_diagnostics_pass_report()
        super().next_status('failed')

    def on_diagnostics_passed(self):
        super().send_diagnostics_pass_report()
        super().clear_alarm()
        super().next_status('standby')

    def on_operator_inservice(self):
        super().abort_diagnostics()
        super().on_operator_inservice()


class Failed(OutOfService):
    def __init__(self, HierachicalStateMachine):
        self._hsm = HierachicalStateMachine


def test():
    """
    >>> hsm = HierachicalStateMachine()
    >>> hsm._current_state
    <__main__.Standby ...

    >>> hsm._next_state('missing')
    Traceback (most recent call last):
    ...
    UnsupportedState

    >>> hsm.on_message('trigger')
    Traceback (most recent call last):
    ...
    UnsupportedMessageType

    >>> hsm._current_state
    <__main__.Standby ...

    >>> hsm._next_state('active')
    >>> hsm._current_state
    <__main__.Active ...

    >>> hsm.on_message('switchover')
    >>> hsm._current_state
    <__main__.Active ...

    >>> hsm.on_message('fault trigger')
    >>> hsm._current_state
    <__main__.Suspect ...

    >>> hsm.on_message('diagnostics failed')
    Traceback (most recent call last):
    ...
    UnsupportedTransition

    >>> hsm.on_message('diagnostics passed')
    Traceback (most recent call last):
    ...
    UnsupportedTransition

    >>> hsm.on_message('operator inservice')
    Traceback (most recent call last):
    ...
    UnsupportedTransition
    """


if __name__ == "__main__":
    # test()
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
