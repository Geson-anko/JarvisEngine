# Jarvis Engine
複雑な並列処理を伴うAIアプリケーションのためのAIエンジン

### 目的
JarvisEngineは次の4つの目的のうちの3番目を達成するために作られました。
1. AIモデルの作成、学習、評価の流れを効率化する。
2. AIが中心となるアプリケーションの作成、デバッグ、リリースを効率化する
3. 複雑な並列処理を伴うAIアプリケーションの作成
4. サーバー上へのデプロイ、ゲームエンジンなどとの連携

# プラットフォーム
- OS
    - Linux
    - WSL
    - macOS 
    - Windows (非推奨)

- Python
    - 3.9以上
# インストール
次のコマンドを実行してインストールします。
```sh
pip install git+https://github.com/Geson-anko/JarvisEngine.git@main
```

### ソースからインストール
ソースからインストールする場合はこのリポジトリをクローンし、JarvisEngineのプロジェクト内で次のコマンドを実行してください。
```sh
pip install -e .
```

# さあ始めよう！
JarvisEngineのインストールが完了しましたね！早速動かしてみましょう。  

1. プロジェクトの作成
    次のコマンドでテンプレートプロジェクトを作成することができます。
    ```sh
    python -m JarvisEngine create -d MyProject
    ```
    次のようなファイルができます。
    ```
    MyProject
    ├── app.py
    └── config.json5
    ```

2. JarvisEngineを起動する  
    次のコマンドでJarvisEngineを起動し、先ほど作成したプロジェクトを実行します。  
    ```sh
    python -m JarvisEngine run -d MyProject
    ```
    - コンソールアウトプット
    ```
    2022/06/02 10:30:13.278 logging_server.server [INFO]: About starting Logging Server...
    2022/06/02 10:30:13.279 MAIN [INFO]: JarvisEngine launch.
    2022/06/02 10:30:13.338 Launcher [INFO]: launch
    2022/06/02 10:30:13.340 Launcher [DEBUG]: periodic update
    2022/06/02 10:30:13.340 Launcher.MyApp [INFO]: launch
    2022/06/02 10:30:13.341 Launcher.MyApp [INFO]: Started!
    2022/06/02 10:30:13.341 Launcher.MyApp [DEBUG]: periodic update
    2022/06/02 10:30:13.341 Launcher.MyApp [INFO]: Updating in 10.00 fps.
    2022/06/02 10:30:13.444 Launcher.MyApp [INFO]: Updating in 10.00 fps.
    2022/06/02 10:30:13.544 Launcher.MyApp [INFO]: Updating in 10.00 fps.
    ...
    ```

    `Enter`キーを押して終了します。
    - コンソールアウトプット
    ```
    ...
    2022/06/02 10:30:13.960 Launcher.MyApp [INFO]: Updating in 10.00 fps.
    2022/06/02 10:30:14.064 Launcher.MyApp [DEBUG]: terminate
    2022/06/02 10:30:14.065 Launcher [DEBUG]: terminate
    2022/06/02 10:30:14.075 logging_server.server [INFO]: Shutdown Logging Server...
    2022/06/02 10:30:14.075 MAIN [INFO]: JarvisEngine shutdown.
    ```

# 次のステップ
JarvisEngineを動作させることができましたか？  
つぎはチュートリアルです。`Tutorial.ja.md`を開きましょう。



