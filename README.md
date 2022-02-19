[![Discord invite link](https://img.shields.io/discord/896668963709255680?color=blue&label=Discord&style=for-the-badge)](http://nekozouneko.ddns.net/discord)
# NKZNK - Discord Bot

NKZNKは、TEAM Nekozouneko により開発されたDiscord Botです。

<img src="https://user-images.githubusercontent.com/70869837/154792369-32cf9d32-82d4-42de-a127-ae50b2a5a6e8.png" width="256">

# 改造方法

このBotの改造には以下の環境が必要です。

- Python 3.8.x 以上をインストール済み
- pipとgitが使用可能

### レポジトリをクローンする
まずはこのレポジトリからファイルをクローンしましょう。
以下のコマンドを実行してください。
```bash
git clone https://github.com/TEAMNekozouneko/NKZNK
```
### モジュールをインストール
そしたら以下のコマンドで必要モジュールをインストールします。
```bash
# Windows
py -3 -m pip install git+https://github.com/Pycord-Development/pycord
py -3 -m pip install mcstatus
py -3 -m pip install aioconsole

# Linux / MacOS
python3 -m pip install git+https://github.com/Pycord-Development/pycord
python3 -m pip install mcstatus
python3 -m pip install aioconsole
```
### 実行
あとはmain.pyにトークンを入れれば以下のコマンドで実行できます。
```bash
# Windows (main.py実行でも可)
./start.bat

# Linux / MacOS (main.py実行でも可)
./start.sh
