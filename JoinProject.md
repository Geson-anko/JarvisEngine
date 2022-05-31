# Jarvis Engine
Jarvis engine is an AI Engine for complex processing, parallel processing, and even linking with game engines.

## How to install Jarvis engine
To install Jarvis engine, please follow the steps below. Note that Anaconda is required to install Jarvis engine.

1. Create new environment in conda. Then activate the environment.
```bash
conda create -n JE python=3.9
conda activate JE
```
2. Install poetry in conda.
```bash
conda install poetry -c conda-forge
```
3. Clone the repository into your computer.
```bash
git clone https://github.com/Geson-anko/JarvisEngine.git
```
4. Change directory to JarvisEngine. Then switch to dev branch.
```bash
cd JarvisEngine
git checkout dev
```
5. Run install command with poetry.
```bash
poetry install
```

## Validation
By running 'TestEngineProject', You can confirm complete installation of Jarvis Engine.
```bash
python -m JarvisEngine run -d TestEngineProject
```

