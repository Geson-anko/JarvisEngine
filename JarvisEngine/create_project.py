import os
from .core import parsers, logging_tool
from .constants import ENGINE_PATH,DEFAULT_CONFIG_FILE_NAME

# The absolute path to the template project
TEMPLATE_PROJECT_PATH = os.path.join(ENGINE_PATH, "template_project")

# The absolute path to the template config file.
TEMPLATE_CONFIG_FILE_PATH = os.path.join(TEMPLATE_PROJECT_PATH, DEFAULT_CONFIG_FILE_NAME)

# The absolute path to the template application file
TEMPLATE_APP_FILE_PATH = os.path.join(TEMPLATE_PROJECT_PATH,"app.py")


def create():
    """create JE project."""
    args = parsers.at_creating()

def make_project_folder(creating_dir:str) -> None:
    """If creating_dir does not exist, make it to disk."""
    if os.path.isdir(creating_dir):
        return
    else:
        os.makedirs(creating_dir)
