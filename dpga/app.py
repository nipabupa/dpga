import ctypes
from typing import Callable
from tkinter import filedialog, messagebox
import dearpygui.dearpygui as dpg
from contextlib import contextmanager

from dpga.utils import create_uuid
from .theme import Size, Style


FONTS = 'assets/fonts.json'
IMGS = 'assets/imgs'


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
    # 创建UUID
    create_uuid(Style)
    for obj in views:
        create_uuid(obj)
    # 加载字体, 主题
    Style.load_fonts(FONTS)
    Style.load_imgs(IMGS)


def _common_ui():
    """公共UI
    """
    # 拖拽
    with dpg.handler_registry():
        dpg.add_mouse_drag_handler(button=0, threshold=0.0, callback=_drag_viewport)


@contextmanager
def build_app(info: AppInfo, views=[]):
    # 启动APP
    dpg.create_context()
    _prepare(info, views)
    dpg.create_viewport(
        title=info.app_name,
        width=600, height=200,
        min_width=info.min_width, min_height=info.min_height,
        resizable=info.resizable,
        decorated=True)
    win = dpg.add_window()
    dpg.set_primary_window(win, True)
    dpg.push_container_stack(win)
    _common_ui()
    yield
    dpg.pop_container_stack()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def _drag_viewport(sender, app_data):
    _, drag_dx, drag_dy = app_data
    drag_start_y = dpg.get_mouse_pos(local=False)[1] - drag_dy
    if drag_start_y < 40:
        x_pos, y_pos = dpg.get_viewport_pos()
        dpg.set_viewport_pos((x_pos + drag_dx, max(0, y_pos + drag_dy)))  # type: ignore
