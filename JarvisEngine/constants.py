import os

# Absolute path to the JarvisEngine directory.
ENGINE_PATH = os.path.split(os.path.abspath(__file__))[0]

# Absolute path to the default_config.toml.
DEFAULT_ENGINE_CONFIG_FILE = os.path.join(ENGINE_PATH, "default_engine_config.toml")

# The default value of project config file name.
DEFAULT_CONFIG_FILE_NAME = "config.json"

# The name of value that tells `shutdown` of JarvisEngine to all apps.
SHUTDOWN_NAME = "shutdown"
