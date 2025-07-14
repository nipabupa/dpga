import dearpygui.dearpygui as dpg
from contextlib import contextmanager


@contextmanager
def vbox():
    """
    纵向stack布局
    """
    uuid = dpg.add_group()
    dpg.push_container_stack(uuid)
    yield uuid
    dpg.pop_container_stack()


@contextmanager
def hbox(space: int = 10):
    """横向stack布局

    Args:
        space (int, optional): 间距. 默认是10

    Yields:
        _type_: UUID
    """
    uuid = dpg.add_group(horizontal=True, horizontal_spacing=space)
    dpg.push_container_stack(uuid)
    yield uuid
    dpg.pop_container_stack()


@contextmanager
def table(columns: int | list[tuple[str, int]], border: tuple[bool, bool, bool, bool] = (True, True, True, True)):
    """创建Table容器

    Args:
        header (int | list[tuple[str, int]], optional): 列信息，数字表示列数且不显示表头；元组列表表示具体列信息并显示表头，其中1号位为列名，2号位为宽度，0表示自适应，1表示最大化，其他数字表示具体宽度尺寸. Defaults to [].
        border (bool, optional): 是否显示边框，分别为外部横线，外部竖线，内部横线，内部竖线. 默认为全显示

    Yields:
        _type_: _description_
    """
    if isinstance(columns, int):
        header = False
    else:
        header = True
    uuid = dpg.add_table(header_row=header, borders_outerH=border[0], borders_outerV=border[1], borders_innerH=border[2], borders_innerV=border[3])
    dpg.push_container_stack(uuid)
    if isinstance(columns, list):
        for label, v in columns:
            if v == 0:
                dpg.add_table_column(label=label, width_fixed=True)
            elif v == 1:
                dpg.add_table_column(label=label, width_stretch=True)
            else:
                dpg.add_table_column(label=label, width=v)
    else:
        for _ in range(columns):
            dpg.add_table_column(width_stretch=True)
    yield uuid
    dpg.pop_container_stack()
