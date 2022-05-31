import os
from JarvisEngine import create_project
from JarvisEngine.create_project import (
    TEMPLATE_PROJECT_PATH, TEMPLATE_CONFIG_FILE_PATH, TEMPLATE_APP_FILE_PATH
)
from JarvisEngine.constants import DEFAULT_CONFIG_FILE_NAME

def test_TEMPLATE_PROJECt_PATH():
    assert os.path.isdir(TEMPLATE_PROJECT_PATH)
    assert TEMPLATE_PROJECT_PATH == os.path.join(
        os.getcwd(),"JarvisEngine", "template_project"
    )

def test_TEMPLATE_APP_FILE_PATH():
    assert os.path.isfile(TEMPLATE_APP_FILE_PATH)
    assert TEMPLATE_APP_FILE_PATH == os.path.join(TEMPLATE_PROJECT_PATH, "app.py")

def test_TEMPLATE_CONFIG_FILE_PATH():
    assert os.path.isfile(TEMPLATE_CONFIG_FILE_PATH)
    assert TEMPLATE_CONFIG_FILE_PATH == os.path.join(
        TEMPLATE_PROJECT_PATH, DEFAULT_CONFIG_FILE_NAME
    )