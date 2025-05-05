import os
from importlib import import_module

apps_registry = {}

def register_apps():
    plugins_path = os.path.join(os.path.dirname(__file__), 'plugins')
    for module_name in os.listdir(plugins_path):
        if module_name == '__pycache__':
            continue
        try:
            module = import_module(f'iia.plugins.{module_name}')
            apps_registry[module.PATH_NAME] = module.APP_NAME
            # module.run_register_app()
        except ImportError:
            print("Error")
