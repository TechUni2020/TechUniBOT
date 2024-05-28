# Discord Bot for Tech.Uni

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/TechUni2020/TechUniBOT/deploy.yml?branch=master&label=build%20(master))
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/TechUni2020/TechUniBOT/deploy.yml?branch=develop&label=build%20(develop))
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/TechUni2020/TechUniBOT)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/TechUni2020/TechUniBOT/discord.py)

## 使用技術
- Python: 3.12.x
- [discord.py](https://github.com/Rapptz/discord.py)
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

## Contributors ✨

Thanks goes to these wonderful people!!

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/KO1231"><img src="https://github.com/TechUni2020/TechUniBOT/assets/124903312/d3317ef0-f926-42b3-9643-dc79f7e3711b" width="100px;" alt=""/><br /><sub><b>岡 和寛</b></sub></a>
    <td align="center"><a href="https://github.com/gohan5858"><img src="" width="100px;" alt=""/><br /><sub><b>足立 里空</b></sub></a>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
