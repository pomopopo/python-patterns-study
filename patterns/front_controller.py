#!/usr/local/bin/python3
"""
*原作者  Gordeev Andrey <gordeev.and.and@gmail.com>

*概要
为控制及消息的请求处理, 提供集中入口
"""


class MobileView:
    def show_index_page(self):
        print('Displaying mobile index page')


class TabletView:
    def show_index_page(self):
        print('Displaying tablet index page')


class Request:
    mobile_type = 'mobile'
    tablet_type = 'tablet'

    def __init__(self, request):
        self.type = None
        request = request.lower()
        if request == self.mobile_type:
            self.type = self.mobile_type
        elif request == self.tablet_type:
            self.type = self.tablet_type


class Dispatcher:
    def __init__(self):
        self.mobile_view = MobileView()
        self.tablet_view = TabletView()

    def dispatch(self, request):
        if request.type == Request.mobile_type:
            self.mobile_view.show_index_page()
        elif request.type == Request.tablet_type:
            self.tablet_view.show_index_page()
        else:
            # print(f'Cannot dispath request: {request}, {request.__dict__}')
            print(f'Cannot dispath request')


class RequestController:
    def __init__(self):
        self.dispatcher = Dispatcher()

    def dispatch_request(self, request):
        if isinstance(request, Request):
            self.dispatcher.dispatch(request)
        else:
            print('request must be a Request object')


def main():
    """
    # 要先有 request controller, 再去 dispatch 具体的 Request
    >>> front_ctlr = RequestController()
    >>> front_ctlr.dispatch_request(Request('mobile'))
    Displaying mobile index page

    >>> front_ctlr.dispatch_request(Request('tablet'))
    Displaying tablet index page

    >>> front_ctlr.dispatch_request(Request('desktop'))
    Cannot dispath request

    >>> front_ctlr.dispatch_request('mobile')
    request must be a Request object
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
