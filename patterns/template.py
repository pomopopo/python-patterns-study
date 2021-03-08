#!/usr/local/bin/python3
"""
*本例
模板模式的一个python实现. python 实现模板和一些静态语言不同,
不需要用类, 直接函数就行.

*应用场景?
- 网页的框架模板
- 算法的各个逻辑系统

*概述
定义了一个基础算法的框架, 将具体步骤的定义延迟到子类中.
"""


def get_text():
    return 'plain-text'


def get_pdf():
    return 'pdf'


def get_csv():
    return 'csv'


def convert_to_text(data):
    print('[CONVERT]')
    return f'{data} as text'


def saver():
    print('[SAVE]')


def template_function(getter, converter=False, to_save=False):
    data = getter()
    print(f'Got `{data}`')

    if len(data) <= 3 and converter:
        data = converter(data)
    else:
        print('Skip convertion')

    if to_save:
        saver()

    print(f'`{data}` was processed')


def main():
    """
    >>> template_function(get_text, to_save=True)
    Got `plain-text`
    Skip convertion
    [SAVE]
    `plain-text` was processed

    >>> template_function(get_pdf, converter=convert_to_text)
    Got `pdf`
    [CONVERT]
    `pdf as text` was processed

    >>> template_function(get_csv, to_save=True)
    Got `csv`
    Skip convertion
    [SAVE]
    `csv` was processed
    """


if __name__ == "__main__":
    # main()
    import doctest
    doctest.testmod(verbose=True)

    # 如果疯了, 所有条件都试一遍也是可以的
    # templates = [template_function(g, c, s)
    #             for g in (get_text, get_pdf, get_csv)
    #             for c in (False, convert_to_text, False)
    #             for s in (True, False, True)]
    # for t in templates:
    #     if t:
    #         t()

