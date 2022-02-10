[![Discord invite link](https://img.shields.io/discord/896668963709255680?color=blue&label=Discord&style=for-the-badge)](http://nekozouneko.ddns.net/discord)
# NKZNK - Discord Bot

NKZNKは、TEAM Nekozouneko により開発されたDiscord Botです。
現在試験版であり開発中です。

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

# Linux / MacOS
python3 -m pip install git+https://github.com/Pycord-Development/pycord
python3 -m pip install mcstatus
```
### 実行
あとはmain.pyにトークンを入れれば以下のコマンドで実行できます。
```bash
# Windows (main.py実行でも可)
./start.bat

# Linux / MacOS (main.py実行でも可)
./start.sh
