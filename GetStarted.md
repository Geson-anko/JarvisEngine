# Get Started
まずはターミナルを開き、次のコマンドを入力してプロジェクトを作成します。

```
python -m JarvisEngine create -n=MyProject
```

そうすると今のフォルダの配下に次のような構造のプロジェクトが出来ます。

```
MyProject  
|- config.json5
|- App
   |- __init__.py
   |- config.json5
   |- app.py
```

### JarvisEngineを起動する

先ほどのコマンドを実行したディレクトリの内部でJarvisEngineを起動します。  
さあこのコマンドを実行しましょう！

```
cd MyProject
python -m JarvisEngine run ./
```
（最後の `./` は省略可能です。）

`console output`
```
YYYY/mm/dd HH:MM:ss,msec main [INFO]: JarvisEngine launch.
...
```

ctrl + c で終了します。

### Tutorials 

各ファイルの中身は次のようになっています。

config.json5
```json5
{
    applications:{
        FpsViewer:{ // 各プロセスの動作frame_rateを見るためのアプリケーション
            path: "JarvisEngine.apps.FpsViewer",
            thread: true, // threading モジュールを使用して並列処理を行います。
                          // falseの場合, multiprocessing モジュールを使用します。
        },
        App:{
            path: "App.app.App", // プロジェクトの直下からimportされます。
            thread: true
        }
    }
}
```

App/config.json5
```json5
{
    frame_rate: 1, // app.pyのAppクラス（このアプリケーション）の実行するFrame rate

    applications: {
        // Appフォルダー直下に Appと同じ構成のアプリケーションを置くことで
        // App内でさらに別のアプリケーションを起動出来ます。
    }
}
```

`App/app.py`
```py
from JarvisEngine.apps import BaseApp

class App(BaseApp):

    def Start(self):
        "`Start` method is called at begin of process!"
        self.logger.info("started.")

    def Update(self):
        "`Update` method is called every frame!"
        self.logger.info(f"Updating in {self.frame_rate} fps.")
```

# 詳細仕様
プロジェクト直下のconfig.json5は実際にはJarvisEngineのメインアプリケーションである `Launcher` アプリケーションクラスのconfigファイルです。

各アプリーケーションは別のアプリケーションを内包し起動することが出来ます。

`Example Project`
```
ExampleProject
|- config.json5
|- App1
|   |- __init__.py
|   |- config.json5
|   |- app.py
|   |- App1_1
|   |   |- __init__.py
|   |   |- config.json5
|   |   +- app.py
|   |
|   |- App1_2
|   |   |- __init__.py
|   |   |- config.json5
|   |   +- app.py
```

`App1/config.json5`のapplicationsは次のように書くことが出来ます。
```json5
{
    frame_rate: 1, // app.pyのAppクラス（このアプリケーション）の実行するFrame rate

    applications: {
        app1_1:{
            path: "App1_1.app.AppClass", // 相対パス。App1 をルートフォルダ
                                         // として扱えます。
            thread: true,
        },
        app1_2:{
            path: "App1.App1_2.app.AppClass", // プロジェクトからの絶対パスも
                                              // 使用できますが移動性が損なわれます。
            thread: true,
        }
    }
}
```

このとき各アプリケーションはこのような形で起動します。`MAIN`はJarvisEngineの`Launcher`クラスです。この名前が各アプリケーションプロセス・スレッドの名前となります。  
この名前は次に登場するプロセス・スレッド間コミュニケーションをする際に必要になります。
またこの名前は アプリケーションの`self.name`属性で参照することが出来ます。
```
MAIN
|- MAIN.App1
|   |- MAIN.App1.App1_1
|   |- MAIN.App1.App1_2
```


アプリケーションのconfigファイルを変更したい場合は、`CONFIG_FILE` 属性をオーバーライドしてください。
```py
from JarvisEngine.apps import BaseApp

class MyApp(BaseApp):
    CONFIG_FILE = "my_config.json"
    def Start(self):
        ...
    
    def Update(self):
        ...
```


# 値の共有
JarvisEngineは各アプリケーションのプロセス・スレッド間コミュニケーションをサポートしています。
各アプリケーションは、メモリが共有された状態の `Thread` 間での値共有と、インタプリターごと分けられた `Process` 間での値共有の２つの場合があります。

以下のではアプリケーションが次のように起動し、動作しているとします。
```
MAIN
|- MAIN.App1
|   |- MAIN.App1.App1_1
|   |- MAIN.App1.App1_2
```

### Process 間での値共有

値を登録するにはアプリケーションに置いて `SetProcessSharedValues`メソッドを実装します。  
プロセス間で値共有を行う場合は、`multiprocessing`モジュールの共有オブジェクトでなければなりません。   
引数の`manager` は `multiprocessing.Manager()`によって生成されたSyncManagerクラスのインスタンスです。
返り値は名前とオブジェクトのタプルのリスト `list[(name, object), ...]` でなければなりません。

__mp.Queueやmp.Valueにより生成されたSynchronizedオブジェクトはUnPicklableなので例え自分自身で参照するためのものだとしてもプロセス開始前に呼ばれる関数内でselfに属性追加してはいけません！__


```py
import multiprocessing as mp

class App(BaseApp):
    ...
    def SetProcessSharedValues(self, manager): # この関数は各アプリの開始前に一度だけ呼ばれます
        
        Queue = mp.Queue()
        Pipe = mp.Pipe()
        return [("MyQueue", Queue), ("MyPipe", Pipe)]     
    ...
```
これを`MAIN.App1.App1_1`が行ったとすると*絶対パス* で次のように登録されます。
```
MAIN.App1.App1_1.MyQueue -> Queue
MAIN.App1.App1_1.MyPipe  -> Pipe
```
この使用により他のアプリが同じ名前を使用していても衝突をしにくくなります。

この共有された`MAIN.App1.App1_1.MyQueue`を参照する際は以後で説明する `オーバーライド可能な関数`の中で`self.getProcessSharedValue`を使用してください。
```py
class App(BaseApp):
    ...
    def Start(self):
        self.App1_Queue = self.getProcessSharedValue("MAIN.App1.App1_1.MyQueue")
```

この参照の仕方には複数ありますので、`共有値の取得方法`をご覧ください。

### Thread 間での値共有
Thread間ではどんな値でも共有することが可能です。共有するためには`SetThreadSharedValues`をオーバーライドし、実装してください。戻り値は`list[(name, Any), ...]`です。

```py
class MyApp(BaseApp):
    ...
    def SetThreadSharedValues(self):
        self.shard_value = 1
        return [("MyApp", self)]
```
取得する際は`getThreadSharedValues`を使用します。詳しくは`共有値の取得方法`を参照ください。

### 共有値の取得方法
プロセス、スレッド間で共有された値を取得するには`getThreadSharedValue`や`getProcessSharedValue`を使用します。

どちらも同じような方法で共有された値を取得することが出来ます。
アプリケーションの移動に関する利便性から、取得には後述する`相対パス`を使用することを推奨します。  
  
`MAIN.App1.App1_1` というアプリが `Queue` という名前で値を共有したとします。
内部的には`MAIN.App1.App1_1.Queue`という名前でオブジェクトが共有されています。

- 絶対パス  
    `MAIN.App1.App1_1.Queue`を直接指定します。
    ```py
    ...
    def Start(self):
        queue = self.getProcessSharedValue("MAIN.App1.App1_1.Queue")
    ...
    ```

- 相対パス  
    自分自身が共有したオブジェクトを取得する際には `.`を先頭につけて指定します。  
    App1_1
    ```py
    ...
    def Start(self):
        my_queue = self.getProcessSharedValue(".Queue")
    ...
    ```
    "."の数だけ階層を遡って取得します。  
    `MAIN.App1`が`Pipe`という名前のオブジェクトを共有していたとすると、`MAIN.App1.App1_1`では次のように取得出来ます。  
    App1_1.py
    ```py
    ...
    def Start(self):
        app1_pipe = self.getProcessSharedValue("..Pipe")
    ...
    ```
    もしディレクトリ構造を変えて`MAIN.App1_1`とした場合に `..Pipe`を取得しようとすると`MAIN`から参照されることに注意してください。



# BaseApp
`JarvisEngine.apps.BaseApp`はアプリケーションの基底クラスであり、このクラスを継承して各アプリケーションは制作されます。

### 属性
- name  
    プロセスまたはスレッドネームであり、アプリケーションの木構造を表します。
    プロパティです。  
    > Ex. `MAIN.App1.App1_1`  

- CONFIG_FILE   
    そのアプリケーションのconfigファイルのパスです。  
    `app.py`と同じディレクトリからの相対パスで指定します。相対パスで読み込めなかった場合はそのパスをそのまま使用します。

- frame_rate  
    `Update`メソッドを実行するframe rateです。configファイルから指定しますが、可変です。
    - 1 >= の時  
        Update関数を実行するFPSです。Update関数を読んでから時間が余る場合は`time.sleep`で休止します。  
    - -1 の時  
        Update関数を一度のみ実行します。  
    - 0 の時  
        実行できる最大のframe_rateで`Update`メソッドを呼び出します。

- PROJECT_DIR  
    プロジェクトまでの絶対パスです。

- APP_DIR
    実行するアプリまでの絶対パスです。

### オーバーライド可能な関数
- プロセス・スレッド開始前に呼ばれる関数
    - Init(self) -> None  
        `BaseApp`のコンストラクタの内部で呼ばれます。

    - SetProcessSharedValues(self, manager) -> List[(str, Any)]  
        プロセス間で共有する値を返す関数です。
        開始前に一度呼ばれます。

- プロセス後に呼ばれる関数
    - SetThreadSharedValues(self) -> List[(str, Any)]  
        スレッド間で共有する値を返す関数です。
        プロセスのヘッドアプリから呼び出されます。  
        この関数で登録された共有値は相対参照することが望ましいです。  
         
- プロセス・スレッド後に呼ばれる関数
    - Awake(self) -> None  
        開始直後に呼ばれる関数です。

    - Start(self) -> None  
        値共有が終了し、アプリケーションの事前準備が終わった後に1度だけ呼ばれます。

    - Update(self, deltatime:float) -> None  
        引数の`deltatime`は前回の`Update`からの経過時間です。
        毎フレーム呼ばれる関数です。
        self.frame_rate = -1の時は一度だけ呼ばれます。
        self.frame_rate >= 1 の時は処理が追いつく限りそのframe_rateで呼ばれます。
    
    - End(self) -> None  
        Engineが終了する際に呼ばれます。この後にBaseApp側のEnd処理が行われます。

    - Terminate(self) -> None  
        アプリが終了する直前に呼ばれます。


### 関数
- launch(self, process_shared_values, thread_shared_values=None)   
    アプリケーションの起動メソッドです。
    オーバライドしてはいけません。

- set_thread_shared_value(name:str, obj:Any)  
    スレッド間共有オブジェクトを登録する関数です。  
    プロセス・スレッド後に値を共有する場合に使います。
    `mp.Process`はメモリが共有されないため、プロセス後に値を共有するための`set_process_shared_value`は実装されません。

# JarvisEngineの起動
JarvisEngineを起動する際にはいくつかのオプションが存在します。  
`python -m JarvisEngine` の後にオプションは付きます。

- run  
    JarvisEngineを起動します。
    runの次にJarvisEngineで起動するプロジェクトのディレクトリパスを指定してください。

    - 第２引数 or `--project_dir`  
        Ex.  
        `python -m JarvisEngine run ./`  
        `python -m JarvisEngine run --project_dir=./`

    - `--log_level` or `-ll`  
        python標準のlogging モジュールに従います  
        Ex. `--log_level=DEBUG`, `-ll=INFO`
- create  
    JarvisEngineを起動するプロジェクトのテンプレートを生成します。  
    - `-n`, `--name`  
        プロジェクトの名前です。  無い場合は`JETemplateProject`というフォルダが作成されます。
        Ex. `-n=MyProject`, `--name=MyProject`  

    - `--target_dir`, `-t`  
        テンプレートを作成するディレクトリです。このディレクトリの中にTemplate Projectの内容がコピーされます。上書きされることもあるので気をつけてください。




