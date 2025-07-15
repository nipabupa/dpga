import sys
import os


class _Resource:

    def __init__(self) -> None:
        self.root = ''
        self.assets = ''
        self.common = ''

    def init(self, app_name: str):
        """
        资源路径
            如果pyinstaller打包
                - 公共资源路径: internal/assets
                - 项目源路径: internal/assets
                - 项目路径: internal/app_name
            如果开发模式(单APP)
                - 公共资源路径: ./assets
                - 项目资源路径: ./assets
                - 项目根路径: ./app_name
            如果开发模式(多APP)
                - 公共资源路径: ./assets
                - 项目资源路径: ./assets/app_name
                - 项目根路径: ./apps/app_name

        Args:
            app_name (str): app名
        """
        if getattr(sys, 'frozen', False):
            if os.path.exists('_internal'):
                self.common = os.path.join('_internal', 'assets')
                self.assets = os.path.join('_internal', 'assets')
                self.root = os.path.join('_internal', app_name)
            else:
                self.common = './assets'
                self.assets = './assets'
                self.root = os.path.join('.', app_name)
        else:
            tmp = os.path.join('.', app_name)
            if os.path.exists(tmp):
                self.common = './assets'
                self.assets = './assets'
                self.root = tmp
            else:
                self.common = './assets'
                self.assets = os.path.join('./assets', app_name)
                self.root = os.path.join('./apps', app_name)


Resource = _Resource()
