# Discord Bot for Tech.Uni

## 使用技術
- Python: 3.12.x
- [discord.py](https://github.com/Rapptz/discord.py): latest
- [Pipenv](https://github.com/pypa/pipenv) (for package management)

## セットアップ
### ① Pythonのインストール
このリポジトリではPython 3.12.x を使用しています。\
Python 3.12.x がインストールされていない場合は、[公式サイト](https://www.python.org/downloads/)からインストールを行うか、[Pyenv](https://github.com/pyenv/pyenv)をインストールしましょう。

### ② pipenvのインストール
このリポジトリではパッケージの管理に pipenv を使用しています。\
まずは pipenv がインストールされているか確認しましょう。
```
pipenv --version
```
上記コマンドを入力してバージョンが表示されたら、すでにpipenvがインストールされているので次に進んでください。

pipenvがインストールされていない場合は、
```
pip install pipenv
```
上記コマンドを入力してpipenvをインストールしましょう。

### ③ リポジトリのクローン
このリポジトリをローカル環境にクローンしましょう。
```
git clone https://github.com/KO1231/TechUniBOT
```

### ④ パッケージのインストール
依存パッケージをインストールしましょう。パッケージのインストールには pipenv を使用します。\
Python 3.12.x がインストールされていない場合でも、①でPyenvをインストールしている場合はこのタイミングで一緒にPython 3.12.x のインストールもしてくれます。
```
pipenv install
```
以上で、セットアップは完了です。