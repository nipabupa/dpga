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
        self.input_number = base * 10
        self.input_text = base * 8
        self.checkbox = base * 5
        self.window_padding_x = base
        self.window_padding_y = base


class _Style:
    def __init__(self):
        self.uuid_text_font = -1
        self.uuid_primary_button_style = -1
        self.uuid_danger_button_style = -1
        self.uuid_window_dialog_style = -1
        self.uuid_title_style = -1
        self.primary_color = (84, 169, 255, 255)
        self.second_color = (84, 169, 255, 150)
        self.danger_color = (252, 114, 78)
        self.text_normal_color = (206, 206, 206)
        self.text_disabled_color = (118, 118, 118)
        self.frame_normal_color = (49, 49, 53)
        self.frame_active_color = (59, 59, 62)
        self.frame_hover_color = (69, 69, 72)

    def __get_uuid(self, uuid=None):
        if uuid:
            return uuid
        return dpg.last_item()

    def load_fonts(self):
        """
        Args:
            filepath (str): 图片路径
        """
        text_str = ''
        # 字体资源
        fontfile = os.path.join(Resource.assets, 'fonts.txt')
        if os.path.exists(fontfile):
            with open(fontfile, encoding='utf-8') as f:
                text_str = f.read()
        # 创建字体
        with dpg.font_registry():
            dpg.add_font("C:\\Windows\\Fonts\\Dengb.ttf", size=Size.base, tag=self.uuid_text_font)
            dpg.bind_font(self.uuid_text_font)
        # 加载资源
        cache = set()
        for chr in text_str:
            cache.add(ord(chr))
            dpg.add_font_chars(list(cache), parent=self.uuid_text_font)

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
        self.__global_style()
        self.__custom_widget_style()

    def __global_style(self):
        with dpg.theme() as global_theme:
            # 主窗口
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, Size.base, Size.base, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 1, 1, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, Size.base // 2, Size.base // 2, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, Size.base // 2, Size.base // 2, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, Size.base, Size.base, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, Size.base // 2, 0, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, Size.base, Size.base // 2, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, Size.base // 4, Size.base // 4, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (32, 32, 32), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.text_normal_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, self.second_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, self.text_disabled_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, self.frame_normal_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, self.frame_active_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, self.frame_hover_color, category=dpg.mvThemeCat_Core)
            # 内嵌子窗口
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2, 2, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, Size.base // 4, Size.base // 4, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, Size.base, Size.base // 2, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (39, 39, 39), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (39, 39, 39), category=dpg.mvThemeCat_Core)
            # 按钮
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, self.frame_normal_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.frame_active_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.frame_hover_color, category=dpg.mvThemeCat_Core)
            with dpg.theme_component(dpg.mvImageButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, self.frame_normal_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.frame_active_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.frame_hover_color, category=dpg.mvThemeCat_Core)
            with dpg.theme_component(dpg.mvButton, enabled_state=False):
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.text_disabled_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.frame_normal_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.frame_normal_color, category=dpg.mvThemeCat_Core)
            # 选择器
            with dpg.theme_component(dpg.mvCombo):
                dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, Size.base // 4, Size.base // 4, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Button, self.frame_normal_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.frame_active_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.frame_hover_color, category=dpg.mvThemeCat_Core)
            # 勾选框
            with dpg.theme_component(dpg.mvCheckbox):
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, Size.base // 2, Size.base // 2, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 4, 4, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, self.second_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Border, self.frame_hover_color, category=dpg.mvThemeCat_Core)
            # 表格
            with dpg.theme_component(dpg.mvTable):
                dpg.add_theme_color(dpg.mvThemeCol_Border, self.frame_hover_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_CellPadding, Size.base, Size.base // 2, category=dpg.mvThemeCat_Core)
        dpg.bind_theme(global_theme)

    def __custom_widget_style(self):
        with dpg.theme(tag=self.uuid_title_style):
            with dpg.theme_component(dpg.mvText):
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.second_color, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0, category=dpg.mvThemeCat_Core)
        with dpg.theme(tag=self.uuid_primary_button_style):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.primary_color, category=dpg.mvThemeCat_Core)
        with dpg.theme(tag=self.uuid_danger_button_style):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.danger_color, category=dpg.mvThemeCat_Core)

    def set_title(self, uuid=None):
        """设置text为title字体

        Args:
            uuid (int|str, optional): 组件UUID. 默认None.
        """
        uid = self.__get_uuid()
        dpg.bind_item_theme(uid, self.uuid_title_style)

    def set_primary_button(self, uuid=None):
        dpg.bind_item_theme(self.__get_uuid(uuid), self.uuid_primary_button_style)

    def set_danger_button(self, uuid=None):
        dpg.bind_item_theme(self.__get_uuid(uuid), self.uuid_danger_button_style)

    def set_dialog(self, uuid=None):
        dpg.bind_item_theme(self.__get_uuid(uuid), self.uuid_window_dialog_style)

    def set_table(self, uuid=None, frame_padding_x=0, frame_padding_y=0, cell_padding_x=0, cell_padding_y=0):
        with dpg.theme() as tmp:
            with dpg.theme_component(dpg.mvTable):
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, frame_padding_x, frame_padding_y, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_CellPadding, cell_padding_x, cell_padding_y, category=dpg.mvThemeCat_Core)
        dpg.bind_item_theme(self.__get_uuid(uuid), tmp)


# 单例对象
Size = _Size()
Style = _Style()
