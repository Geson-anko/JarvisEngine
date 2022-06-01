import os
import shutil
from JarvisEngine import create_project
from JarvisEngine.create_project import (
    TEMPLATE_PROJECT_PATH, TEMPLATE_CONFIG_FILE_PATH, TEMPLATE_APP_FILE_PATH,
    TEMPLATE_APP_FILE_NAME
)
from JarvisEngine.constants import DEFAULT_CONFIG_FILE_NAME

def test_TEMPLATE_PROJECt_PATH():
    assert os.path.isdir(TEMPLATE_PROJECT_PATH)
    assert TEMPLATE_PROJECT_PATH == os.path.join(
        os.getcwd(),"JarvisEngine", "template_project"
    )


def test_TEMPLATE_APP_FILE_NAME():
    assert TEMPLATE_APP_FILE_NAME == "app.py"

def test_TEMPLATE_APP_FILE_PATH():
    assert os.path.isfile(TEMPLATE_APP_FILE_PATH)
    assert TEMPLATE_APP_FILE_PATH == os.path.join(
        TEMPLATE_PROJECT_PATH, TEMPLATE_APP_FILE_NAME
    )

def test_TEMPLATE_CONFIG_FILE_PATH():
    assert os.path.isfile(TEMPLATE_CONFIG_FILE_PATH)
    assert TEMPLATE_CONFIG_FILE_PATH == os.path.join(
        TEMPLATE_PROJECT_PATH, DEFAULT_CONFIG_FILE_NAME
    )


def test_make_project_folder():
    creating_dir = "_test_project"
    assert not os.path.exists(creating_dir)
    create_project.make_project_folder(creating_dir)
    assert os.path.isdir(creating_dir)

    os.rmdir(creating_dir)
    assert not os.path.exists(creating_dir) # remove after test.

def test_copy_files():
    creating_dir = "_test_project"
    create_project.make_project_folder(creating_dir)
    create_project.copy_files(creating_dir)

    assert os.path.isfile(os.path.join(creating_dir,DEFAULT_CONFIG_FILE_NAME))
    assert os.path.isfile(os.path.join(creating_dir,TEMPLATE_APP_FILE_NAME))
    
    shutil.rmtree(creating_dir)
    assert not os.path.exists(creating_dir)