import time
import dearpygui.dearpygui as dpg
from dpga.app import build_app, AppInfo, start_loading, stop_loading
from dpga.containter import hbox, table
from dpga.theme import Size, Style


info = AppInfo()
info.app_name = 'demo1'
info.title = '示例'
info.base = 15
info.width = 800
info.min_width = 800
info.height = 600
info.min_height = 600
info.resizable = True


def content():
    with hbox(space=20):
        dpg.add_button(label='你好', callback=callback1)
        Style.set_primary_button()
        dpg.add_button(label='你好', callback=callback2)
        Style.set_danger_button()
        dpg.add_button(label='你好')
        dpg.add_button(label='你好')
        dpg.add_button(label='你好', enabled=False)
    with hbox(space=20):
        dpg.add_combo(['A', 'B', 'C'], default_value="A", width=Size.combo)
        dpg.add_combo(['A', 'B', 'C'], default_value="A", width=Size.combo)
        dpg.add_combo(['A', 'B', 'C'], default_value="A", width=Size.combo)
    with dpg.child_window(height=250):
        with hbox(space=20):
            dpg.add_checkbox(label="A")
            dpg.add_checkbox(label='B')
            dpg.add_checkbox(label='C')
        with hbox(space=20):
            dpg.add_input_int(label='A', width=Size.input_number)
            dpg.add_input_text(label='B', width=Size.input_text)
    dpg.add_text('表格')
    Style.set_title()
    with table(3):
        with dpg.table_row():
            dpg.add_button(label='你好')
            dpg.add_button(label='你好')
            dpg.add_button(label='你好')
        with dpg.table_row():
            dpg.add_text('你好')
            dpg.add_text('你好')
            dpg.add_text('你好')
        with dpg.table_row():
            dpg.add_text('你好')
            dpg.add_button(label='你好')
            dpg.add_button(label='你好')


def callback1():
    start_loading()
    time.sleep(3)
    stop_loading()


def callback2():
    start_loading(modal=True)
    time.sleep(3)
    stop_loading()


with build_app(info):
    content()
    with dpg.window():
        content()

