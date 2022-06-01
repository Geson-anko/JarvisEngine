import os
import shutil
from .core import parsers, logging_tool
from .constants import ENGINE_PATH,DEFAULT_CONFIG_FILE_NAME

# The absolute path to the template project
TEMPLATE_PROJECT_PATH = os.path.join(ENGINE_PATH, "template_project")

# The absolute path to the template config file.
TEMPLATE_CONFIG_FILE_PATH = os.path.join(TEMPLATE_PROJECT_PATH, DEFAULT_CONFIG_FILE_NAME)

# The name of application file in template project.
TEMPLATE_APP_FILE_NAME = "app.py"

# The absolute path to the template application file
TEMPLATE_APP_FILE_PATH = os.path.join(TEMPLATE_PROJECT_PATH,TEMPLATE_APP_FILE_NAME)



def create():
    """create JE project."""
    args = parsers.at_creating()

def make_project_folder(creating_dir:str) -> None:
    """If creating_dir does not exist, make it to disk."""
    if os.path.isdir(creating_dir):
        return
    else:
        os.makedirs(creating_dir)

def copy_files(creating_dir:str) -> None:
    """copy file to creating project directory."""

    target_config_file_path = os.path.join(creating_dir, DEFAULT_CONFIG_FILE_NAME)
    target_app_file_path = os.path.join(creating_dir, TEMPLATE_APP_FILE_NAME)

    shutil.copyfile(TEMPLATE_CONFIG_FILE_PATH, target_config_file_path)
    shutil.copyfile(TEMPLATE_APP_FILE_PATH, target_app_file_path)
    
