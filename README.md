# Jarvis Engine
The AI Engine for complex parallel process AI applications.

### Purpose
JarvisEngine is created to achieve 3rd goal out of 4 goals.
1. To improve AI model creation, training, and evaluation flow. 
2. To improve AI-centric application creation, debugging, and releasing.
3. To create AI Application with Complex parallel process.
4. To connect to Servers, and Game Engines.

# Platform
- OS
    - Linux
    - WSL
    - macOS 
    - Windows (deprecated)

- Python
    - 3.9 or above
# Install
Install by running the following command.
```sh
pip install git+https://github.com/Geson-anko/JarvisEngine.git@master
```

### Install from Source
If you are installing from source, clone this repository and run the following command inside Jarvis Engine project:
```sh
pip install -e .
```

# Let's begin!
After installation, Let's try execute JarvisEngine.

1. Create a project
    Create a template project with the following command:
    ```sh
    python -m JarvisEngine create -d MyProject
    ```
    The following files will be created.
    ```
    MyProject
    ├── app.py
    └── config.json
    ```

2. Execute JarvisEngine
    Execute JarvisEngine with the following command, and run the project you created.
    ```sh
    python -m JarvisEngine run -d MyProject
    ```
    - Console output
    ```
    2022/06/02 10:30:13.278 logging_server.server [INFO]: About starting Logging Server...
    2022/06/02 10:30:13.279 MAIN [INFO]: JarvisEngine launch.
    2022/06/02 10:30:13.338 Launcher [INFO]: launch
    2022/06/02 10:30:13.340 Launcher [DEBUG]: periodic update
    2022/06/02 10:30:13.340 Launcher.MyApp [INFO]: launch
    2022/06/02 10:30:13.341 Launcher.MyApp [INFO]: Started!
    2022/06/02 10:30:13.341 Launcher.MyApp [DEBUG]: periodic update
    2022/06/02 10:30:13.341 Launcher.MyApp [INFO]: Updating in 0.10 fps.
    2022/06/02 10:30:13.444 Launcher.MyApp [INFO]: Updating in 0.10 fps.
    2022/06/02 10:30:13.544 Launcher.MyApp [INFO]: Updating in 0.11 fps.
    ...
    ```

    Press the `Enter` key to exit.
    - Console output
    ```
    ...
    2022/06/02 10:30:13.960 Launcher.MyApp [INFO]: Updating in 0.10 fps.
    2022/06/02 10:30:14.064 Launcher.MyApp [DEBUG]: terminate
    2022/06/02 10:30:14.065 Launcher [DEBUG]: terminate
    2022/06/02 10:30:14.075 logging_server.server [INFO]: Shutdown Logging Server...
    2022/06/02 10:30:14.075 MAIN [INFO]: JarvisEngine shutdown.
    ```

# Next step
Did you get the Jarvis Engine working?
Next is the tutorial. Let's open `Tutorial.md`.


