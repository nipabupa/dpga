import dearpygui.dearpygui as dpg
from dpga.app import build_app, AppInfo


info = AppInfo()
info.app_name = 'demo1'
info.title = '示例'
info.base = 15
info.width = 800
info.min_width = 800
info.height = 600
info.min_height = 600
info.resizable = False


with build_app(info):
    dpg.add_button(label='你好')
