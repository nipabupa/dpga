import json
import os
import dearpygui.dearpygui as dpg
from .utils import Resource


class _Size:
    def __init__(self):
        self.base = 20
        self.button = -1
        self.combo = -1
        self.input_number = -1
        self.input_text = -1
        self.checkbox = -1
        self.window_padding_x = -1
        self.window_padding_y = -1

    def set_base(self, base: int):
        self.base = base
        self.button = base * 4
        self.combo = base * 5
        self.input_number = base * 4
        self.input_text = base * 6
        self.checkbox = base * 5
        self.window_padding_x = base
        self.window_padding_y = base


class _Style:
    def __init__(self):
        self.uuid_text_font = -1
        self.uuid_title_font = -1
        self.uuid_primary_button = -1
        self.uuid_danger_button = -1
        self.uuid_window_dialog = -1
        self.primary_text_color = (255, 255, 255, 255)
        self.secondary_text_color = (206, 206, 206, 255)
        self.disabled_text_color = (118, 118, 118, 255)

    def __get_uuid(self, uuid=None):
        if uuid:
            return uuid
        return dpg.last_item()

    def load_fonts(self):
        """
        Args:
            filepath (str): 图片路径
        """
        title_str = ''
        text_str = ''
        # 字体资源
        fontfile = os.path.join(Resource.assets, 'fonts.json')
        print(fontfile)
        if os.path.exists(fontfile):
            with open(fontfile, encoding='utf-8') as f:
                obj = json.load(f)
                title_str = obj.get('title', '')
                text_str = obj.get('text', '')
        # 创建字体
        with dpg.font_registry():
            dpg.add_font("C:\\Windows\\Fonts\\Dengb.ttf", size=Size.base, tag=self.uuid_text_font)
            dpg.add_font("C:\\Windows\\Fonts\\Dengb.ttf", size=Size.base + 3, tag=self.uuid_title_font)
            dpg.bind_font(self.uuid_text_font)
        # 加载资源
        cache = set()
        for chr in text_str:
            cache.add(ord(chr))
            dpg.add_font_chars(list(cache), parent=self.uuid_text_font)
        cache = set()
        for chr in title_str:
            cache.add(ord(chr))
            dpg.add_font_chars(list(cache), parent=self.uuid_title_font)

    def load_imgs(self):
        """加载图片资源

        Args:
            filepath (str): 图片路径
        """
        with dpg.texture_registry():
            width, height, _, data = dpg.load_image(os.path.join(Resource.common, 'minus.png'))
            dpg.add_static_texture(width=width, height=height, default_value=data, tag='minus.png')
            width, height, _, data = dpg.load_image(os.path.join(Resource.common, 'zoom.png'))
            dpg.add_static_texture(width=width, height=height, default_value=data, tag='zoom.png')
            width, height, _, data = dpg.load_image(os.path.join(Resource.common, 'close.png'))
            dpg.add_static_texture(width=width, height=height, default_value=data, tag='close.png')
            filepath = os.path.join(Resource.assets, 'imgs')
            if not os.path.exists(filepath):
                return
            for filename in os.listdir(filepath):
                # 只接受PNG与JPG
                if not filename.endswith('png') and not filename.endswith('jpg'):
                    continue
                width, height, _, data = dpg.load_image(os.path.join(filepath, filename))
                tag = os.path.basename(filename)
                dpg.add_static_texture(width=width, height=height, default_value=data, tag=tag)

    def load_style(self):
        pass

    def set_title(self, uuid=None):
        """设置text为title字体

        Args:
            uuid (int|str, optional): 组件UUID. 默认None.
        """
        dpg.bind_item_font(self.__get_uuid(uuid), self.uuid_title_font)

    def set_primary_button(self, uuid=None):
        dpg.bind_item_theme(self.__get_uuid(uuid), self.uuid_primary_button)

    def set_danger_button(self, uuid=None):
        dpg.bind_item_theme(self.__get_uuid(uuid), self.uuid_danger_button)

    def set_dialog(self, uuid=None):
        dpg.bind_item_theme(self.__get_uuid(uuid), self.uuid_window_dialog)


# 单例对象
Size = _Size()
Style = _Style()
