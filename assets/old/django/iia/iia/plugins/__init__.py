import importlib

import os

def get_subfolder_names(folder_path):
    # 确保提供的路径存在
    if os.path.isdir(folder_path):
        # 使用os.listdir()获取文件夹中的所有文件和子文件夹
        contents = os.listdir(folder_path)

        # 使用列表推导式过滤出子文件夹名
        subfolder_names = [name for name in contents if os.path.isdir(os.path.join(folder_path, name)) and name != '__pycache__']

        return subfolder_names
    else:
        raise ValueError(f"The provided path '{folder_path}' is not a directory.")

# 使用示例
folder_path = './iia/plugins'  # 替换为你的文件夹路径
plugin_names = get_subfolder_names(folder_path)

def import_plugin(plugin_name):
    # 使用importlib来动态导入模块
    return importlib.import_module(f"iia.plugins.{plugin_name}")

data = {}
for name in plugin_names:
    data[name] = import_plugin(name)
