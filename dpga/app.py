import ctypes
import dearpygui.dearpygui as dpg
from contextlib import contextmanager
from typing import Callable
from tkinter import filedialog, messagebox

from .theme import Size, Style
from .utils import Resource


class AppInfo:
    def __init__(self) -> None:
        # APP名, 英文
        self.app_name = ''
        # APP顶部标题
        self.title = ''
        # 宽度
        self.width = 800
        self.min_width = 400
        # 高度
        self.height = 600
        self.min_height = 300
        # 基础尺寸
        self.base = 20
        # 是否可调整大小
        self.resizable = False
        # 关闭回调
        self.on_close: Callable | None = None


def confirm(title: str, msg: str):
    messagebox.askokcancel(title=title, message=msg)


def show_info(msg: str):
    messagebox.showinfo("信息", message=msg)


def show_warning(msg: str):
    messagebox.showwarning("注意", message=msg)


def show_error(msg: str):
    messagebox.showerror("异常", message=msg)


def select_file() -> str:
    return filedialog.askopenfilename()


def select_files() -> list[str]:
    return filedialog.askopenfilenames()  # type: ignore


def select_directory() -> str:
    return filedialog.askdirectory()


def save_file():
    return filedialog.asksaveasfilename()


def start_loading(modal=True):
    if modal and dpg.does_item_exist('backend_loading'):
        dpg.delete_item('backend_loading')
    if modal:
        with dpg.window():
            pass
    else:
        with dpg.window():
            pass


def stop_loading():
    if dpg.does_item_exist('backend_loading'):
        dpg.delete_item('backend_loading')
    if dpg.does_item_exist('modal_loading'):
        dpg.delete_item('modal_loading')


def _prepare(info: AppInfo, views: list):
    # 不感知系统DPI，默认以屏幕最大分辨率渲染，由系统自行缩放
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware(0)
    v = user32.GetDpiForSystem()
    dpi = v // 96
    # 加载尺寸信息
    Size.set_base(info.base * dpi)
    info.width *= dpi
    info.min_width *= dpi
    info.height *= dpi
    info.min_height *= dpi
    # 创建UUID
    _create_uuid(Style)
    for obj in views:
        _create_uuid(obj)
    # 加载字体, 主题
    Style.load_fonts()
    Style.load_imgs()
    Style.load_style()


def _common_ui(info: AppInfo):
    """
    公共UI
    """
    # header
    with dpg.table(header_row=False, borders_outerH=True, borders_innerV=True):
        Style.set_table()
        dpg.add_table_column(width_fixed=True)
        dpg.add_table_column(width_stretch=True)
        dpg.add_table_column(width_fixed=True)
        with dpg.table_row():
            dpg.add_text(info.title)
            dpg.add_spacer()
            with dpg.group(horizontal=True, horizontal_spacing=Size.base // 2):
                if info.resizable:
                    dpg.add_image_button('minus.png',
                                         width=Size.base,
                                         height=Size.window_padding_x,
                                         callback=lambda: dpg.minimize_viewport())
                    dpg.add_image_button('zoom.png',
                                         width=Size.base,
                                         height=Size.window_padding_x,
                                         callback=lambda: dpg.maximize_viewport())
                    dpg.add_image_button('close.png',
                                         width=Size.window_padding_x,
                                         height=Size.window_padding_x,
                                         callback=info.on_close if info.on_close is not None else lambda: dpg.stop_dearpygui())
                else:
                    dpg.add_image_button('minus.png',
                                         width=Size.window_padding_x,
                                         height=Size.window_padding_x,
                                         callback=lambda: dpg.minimize_viewport())
                    dpg.add_image_button('close.png',
                                         width=Size.window_padding_x,
                                         height=Size.window_padding_x,
                                         callback=info.on_close if info.on_close is not None else lambda: dpg.stop_dearpygui())
    # 拖拽
    with dpg.handler_registry():
        dpg.add_mouse_drag_handler(button=0, threshold=0.0, callback=_drag_viewport)


def _create_uuid(obj):
    for attr in dir(obj):
        if attr.startswith('uuid_'):
            setattr(obj, attr, dpg.generate_uuid())


@contextmanager
def build_app(info: AppInfo, views=[]):
    # 初始化全局资源
    Resource.init(info.app_name)
    # 启动APP
    dpg.create_context()
    _prepare(info, views)
    dpg.create_viewport(
        title=info.app_name,
        width=info.width, height=info.height,
        min_width=info.min_width, min_height=info.min_height,
        resizable=info.resizable,
        decorated=False)
    win = dpg.add_window()
    dpg.set_primary_window(win, True)
    dpg.push_container_stack(win)
    _common_ui(info)
    yield
    dpg.pop_container_stack()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def _drag_viewport(_, app_data):
    _, drag_dx, drag_dy = app_data
    drag_start_y = dpg.get_mouse_pos(local=False)[1] - drag_dy
    if drag_start_y < Size.window_padding_y * 3:
        x_pos, y_pos = dpg.get_viewport_pos()
        dpg.set_viewport_pos((x_pos + drag_dx, max(0, y_pos + drag_dy)))  # type: ignore
