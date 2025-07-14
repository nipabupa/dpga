from functools import wraps
import dearpygui.dearpygui as dpg


def singleton(cls):
    _instance = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return wrapper


def create_uuid(obj):
    for attr in dir(obj):
        if attr.startswith('uuid_'):
            setattr(obj, attr, dpg.generate_uuid())
