<!-- 
MIT License

Copyright (c) 2022 Nekozouneko Team Lab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-->

[![Discord invite link](https://img.shields.io/discord/896668963709255680?color=blue&label=Discord&style=for-the-badge)](http://nekozouneko.ddns.net/discord)
# NKZNK - Discord Bot

NKZNKは、TEAM Nekozouneko により開発されたDiscord Botです。

<img src="https://user-images.githubusercontent.com/70869837/154792369-32cf9d32-82d4-42de-a127-ae50b2a5a6e8.png" width="256">

# 改造方法

このBotの改造には以下の環境が必要です。

> Python 3.8.x 以上をインストール済み  
> pipとgitが使用可能

### レポジトリをクローンする
まずはこのレポジトリからファイルをクローンしましょう。
以下のコマンドを実行してください。
```bash
git clone https://github.com/TEAMNekozouneko/NKZNK
```
### モジュールをインストール
そしたら以下のコマンドで必要モジュールをインストールします。
#### Windows
```bash
py -3 -m pip install -r requirements.txt
```

#### Linux / MacOS
```
python3 -m pip install -r requirements.txt
```
### 実行
あとはmain.pyにトークンを入れれば以下のコマンドで実行できます。
#### Windows
```bash
py -3 main.py
```
#### Linux / MacOS
Linuxの場合ロケールの設定が異なっています。
以下のコードに変更してください。

> Cog/EventListener.py
```diff
# 略 

async def presences(self):
    while True:
-       locale.setlocale(locale.LC_TIME, "ja_JP")
+       locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
        today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

# 略
```
そして以下を実行します。
```
python3 main.py
```
