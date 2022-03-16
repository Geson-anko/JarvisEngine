# JarvisEngine
汎用人工知能などの複雑なAIアプリケーションを容易に構築するための AI Engine


# プラットフォーム
- OS
    - Linux
    - Windows 
    - WSL
    - MacOS X

- GPU  
    - NVIDIA CUDA

- Python
    - 3.9
    - 3.10

# 目的
1. AIモデルの作成、学習、評価の流れを効率化する。

2. AIが中心となるアプリケーションの作成、デバッグ、リリースを効率化する

2. 複数のAIモデルを複雑に組み合わせた処理を可能にする
    - AIモデルを常時 稼働/待機 
    - 非同期に 学習/推論   
    <br />
3. サーバー上へのデプロイ、ゲームエンジンなどとの連携

    

# Installation
このリポジトリをクローンし、次のコマンドを実行してインストールします
```shell
pip install -e ./
```
  
次にコマンドを実行して正常にインストールされているか確かめてください。
```shell
python -c "import JarvisEngine as JE;print(JE.__version__)"
```

# Get Started
次のコマンドを実行してみましょう。
```shell
python -m JarvisEngine --log_level=DEBUG
```

console output
```
HH:mm:ss MAIN INFO: Engine launched.
...
```
ctrl + c で終了します
```
...
HH:mm:ss MAIN INFO: Engine shutdown.
```

## Tutorial 
プロジェクトディレクトリを作ります。
そのディレクトリの中で ```TestApp.py``` と ```AppConfig.toml``` いうファイルを作成します。

- TestApp.py

```python 
from JarvisEngine.core import *
from JarvisEngine.app import BaseApp

class MyApp(BaseApp):
    CONFIG_FILE:str = "AppConfig.toml"
    def Start(self):
        """Called when process started."""
        log.info("started")

    def Update(self):
        """Called every frame"""
        log.info()
```

- AppConfig.toml

```
frame_rate = 10
# other...
```

そして ```config.toml``` を作成します。

- config.toml
```
[Applications]
TestApp = "TestApp.MyApp"
# ThreadName = "ModuleName.AppName"
```

実行するスクリプトができました！このスクリプトをJarvisEngineで実行しましょう！
```
python -m JarvisEngine --config=./config.toml --log_level=DEBUG
```

console output
```
...
```










