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


def make_template(skeleton, getter, *arg, **kw):
    """更抽象一级的模板, 可以用来造列表"""
    def template():
        return skeleton(getter, *arg, **kw)
    return template


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

    >>> templates = [make_template(template_function,g, converter=c, to_save=s)
    ...     for g in (get_text, get_pdf, get_csv)
    ...     for c in (False, convert_to_text, False)
    ...     for s in (True, False, True)]
    """

def main2():
    # 如果疯了, 所有条件都试一遍也是可以的
    """
    # 用 make_template 造更灵活的函数, 存入列表
    >>> templates = [make_template(template_function, g, converter=c, to_save=s)
    ...     for g in (get_pdf, get_csv)
    ...     for c in (convert_to_text, False)
    ...     for s in (True,)
    ... ]

    >>> templates
    [<function make_template.<locals>.template at 0x...>, ...]

    >>> for t in templates:
    ...     t()
    Got `pdf`
    [CONVERT]
    [SAVE]
    `pdf as text` was processed
    Got `pdf`
    Skip convertion
    [SAVE]
    `pdf` was processed
    Got `csv`
    [CONVERT]
    [SAVE]
    `csv as text` was processed
    Got `csv`
    Skip convertion
    [SAVE]
    `csv` was processed

    """


if __name__ == "__main__":
    # main()

    import doctest
    doctest.testmod(verbose=True , optionflags=doctest.ELLIPSIS)

