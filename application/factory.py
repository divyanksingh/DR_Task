import os
import importlib
from flask import Flask
from config import app_config

from application.controllers_list import BLUEPRINT_LIST
from application.extensions import register_extension


def register_controllers(app):
    for each_list in BLUEPRINT_LIST:
        module_path_list = each_list.split(".")
        blueprint = module_path_list.pop()
        module_path = ".".join(module_path_list)
        module = importlib.import_module(module_path)
        module = getattr(module, blueprint)
        app.register_blueprint(module)
    return app

def import_models():
    models_package = "models"
    files = os.listdir(models_package)
    for each_file in files:
        if each_file.endswith(".py"):
            importlib.import_module(models_package + "." + each_file[:-3])


def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config[os.getenv('FLASK_CONFIG')])
    app = register_extension(app)
    app = register_controllers(app)
    import_models()
    return app