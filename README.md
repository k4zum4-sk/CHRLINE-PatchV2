# CHRLINE 修正パッチ: 循環インポート & Cryptoエラー対応 (日本語版)
![logo](/examples/assets/logo.png)

このプロジェクトは、Python非公式LINE APIラッパーであるCHRLINEの**循環インポート問題やインポートエラー**などを修正したバージョンです。



# CHRLINEとは？

CHRLINEは、LINEのChrome版APIを利用した非公式ラッパーライブラリです。


CHRLINEを使うことで公式のMessaging APIでは実現できない**様々なデバッグ**や**個人アカウントのBOT化**,**オープンチャットでのBOT活動**などを実現できます。

元々は**Thriftを使用しないLINE Chrome APIの解析ツール**として開発されました。

そのため、通常のbot用途には非推奨とされています（**動作自体は可能です**）

元のCHRLINEリポジトリ -> [DeachSword/CHRLINE](https://github.com/DeachSword/CHRLINE/tree/master)

# 背景
まず、このライブラリの直接の開発者は私ではありません。
**DeachSword氏が全ての権利を保有**します

CHRLINE を利用する際、Crypto モジュールのエラーや、循環インポートの問題が発生することがあります。
そこで、多くのユーザーがスムーズに利用できるよう、これらの問題を修正したパッチを作成しました。

# どんな用途に向いてるか
 - LINEの通信仕様やプロトコルの解析をしたい人
 - 実験的・学習用にLINE Botを試したい人（本番運用は非推奨）
 - TMoreCompactのような公式仕様の挙動を調べたい人

# 応用例①：スクエアBOTの開発

このパッチを適用した環境では、LINEオープンチャット（スクエア）向けのBOTも開発できます。
日本語コメント付きのテスト用BOTコードは `test/square_bot.py` に用意してあります。  
**特定メッセージの検知、音声送信、メッセージ削除**などを試せます。
<div><video controls src="https://github.com/user-attachments/assets/1b442ff2-7ab0-4c68-a944-4311730c430b"></video></div>

# 応用例②：グループBOTの開発

日本語コメント付きのテスト用BOTコードは `test/group_bot.py` に用意してあります。  
**特定メッセージの検知、画像送信、スタンプ検知**などを試せます。
<div><video controls src="https://github.com/user-attachments/assets/ce93d7b3-4b77-4388-9b25-145bbd344530"></video></div>



# 私の小さな貢献
- 元ライブラリのコード解析
- 問題箇所の特定と修正
- テストコードの作成と動作確認

# 具体的な修正内容

**1. Windows環境での Crypto モジュールのエラー修正**
  
  - `from Crypto.Cipher import AES` などのインポートが Windows でエラーになる問題を修正
  - `CHRLINE-PatchV2/CHRLINE/e2ee.py,models.py` のインポート文 `Crypto` を `Cryptodome` に変更し、どの環境でも動作するよう統一

  - もし `pycrypto` をインストールしている場合は、以下のコマンドで削除し、代わりに pycryptodomex をインストールしてください
```sh
python -m pip uninstall pycrypto
python -m pip install pycryptodomex
```

  - 
**2. 循環インポートとそれに関するエラーの修正**

  - `thrift.py` というファイル名が公式の `thriftライブラリ`と衝突して循環インポートを起こしていたので`chrline_thrift.py`にリネーム
  - `client.py`のインポート文を`chrline_thrift`に合わせて修正

## はじめに

このリポジトリをクローンし、セットアップ手順を実行してください

```sh
git clone https://github.com/k4zum4-sk/CHRLINE-PatchV2.git
```
## セットアップ

以下のコマンドでセットアップが実行できます：
```sh
python3 setup.py install
```
上記でダメな場合
```sh
python3 -m pip install .
```
日本語のコメント付きサンプルコードは `CHRLINE-PatchV2/test/` にあります。  

利用可能なAPI一覧は `CHRLINE-PatchV2/CHRLINE/services` から必要なファイルを参照してください。

まずは`CHRLINE-PatchV2/test/login_getToken_test.py`から試してみてください。

`login_getToken_test.py`で取得したトークンを 環境変数 `LINE_AUTH_TOKEN`に設定し、トークンをソース管理下に置かないようにしてください。

**環境変数の設定 FOR MAC & WSL**
1. echo $SHELL を実行し、シェルの種類を確認:
  ```sh
  echo $SHELL
  ```
 - zsh → .zshrc に設定する: ->
   ```sh
   echo 'export CHRLINE_PATCH_PATH="CHRLINE-PatchV2の正しいディレクトリパスを指定"' >> ~/.zshrc
   ```
 - bash → .bashrc に設定する: ->
   ```sh
   echo 'export CHRLINE_PATCH_PATH="CHRLINE-PatchV2の正しいディレクトリパスを指定"' >> ~/.bashrc
   ```
 2. 設定を反映:
 - zsh
   ```sh
   source ~/.zshrc
   ```
 - bash
   ```sh
   source ~/.bashrc
   ```
3. 確認:
   ```sh
   echo $CHRLINE_PATCH_PATH
   ```

**環境変数の設定 FOR WINDOWS**
1. コマンドプロンプト（cmd）の場合:
  ```sh
  set CHRLINE_PATCH_PATH="CHRLINE-PatchV2の正しいディレクトリパスを指定"
  ```
2. PowerShell の場合:
  ```sh
  [System.Environment]::SetEnvironmentVariable("CHRLINE_PATCH_PATH", "CHRLINE-PatchV2の正しいディレクトリパスを指定", [System.EnvironmentVariableTarget]::User)
  ```
  現在のセッションのみで有効 にする場合：
  ```sh
  $env:CHRLINE_PATCH_PATH = "CHRLINE-PatchV2の正しいディレクトリパスを指定"
  ```

# 環境差異に関する注意点

CHRLINEのバージョンや環境によって、`SquareMessage` に含まれるフィールド構造が異なる場合があります。

例えば、`event.payload.notificationMessage.squareMessage.message.text` に直接アクセスできる環境もあれば、  
`event.val_4.val_30.val_2.val_1` のように `.val_xx` を辿らなければならない環境も確認されています。

そのため、環境依存性を避けるために `getattr` での防御的な取得を推奨します。

```sh
text = getattr(notification.squareMessage.message, 'text', '')
```

動作確認済みのCHRLINEは、バージョン`CHRLINE==2.5.24`に本修正パッチを当てた環境です。

#### 必要条件 ####
- CHRLINE
- Python 3.6<
  - ~~pycrypto~~
  - **pycryptodomex**
  - xxhash
  - httpx[http2]
  - gevent
  - thrift
  - rsa
  - python-axolotl-curve25519
  - image
  - requests
  - qrcode
  - cryptography
  - rich

```sh
pip install pycryptodomex xxhash httpx gevent thrift rsa python-axolotl-curve25519 image requests qrcode cryptography rich
```

必要なモジュールが不足している場合は、適宜インストールしてください。

# 注意点
 - **公式のLINE APIではない**ため、利用は自己責任でお願いします。
 - **LINEの規約に違反する可能性があるため、本番環境での利用は推奨しません**。
 - このプロジェクトは**研究・学習目的の利用を前提**としています。

=========================== k4zum4 =========================

# CHRLINE Patch: Fixing Circular Imports & Crypto Errors

First of all, I am not the direct developer of this library.
DeachSword holds all rights to it.

This project is a modified version of the unofficial LINE API, CHRLINE, that fixes circular import issues and import errors.

# My Contribution:
- Analyzed the original library's code to identify issues related to circular imports and Crypto module errors.
- Implemented fixes to ensure compatibility across different environments (e.g., Windows).
- Created and tested login functionality to verify the patch's effectiveness.

# Specific changes:

1. **Fixed Crypto module error on Windows**

  - Resolved an issue where from Crypto.Cipher import AES and similar imports caused errors on Windows.
  
  - Updated import statements in CHRLINE-PatchV2/CHRLINE/e2ee.py and models.py, changing Crypto to Cryptodome to ensure compatibility across all environments.

2. **Fixed circular imports and related errors**

  - The file thrift.py was conflicting with the thrift library, causing circular imports. It has been renamed to chrline_thrift.py to resolve the issue.
  
  - The import statements in client.py were modified to match the changes in chrline_thrift.

The basic usage in Japanese is described in the CHRLINE-PatchV2/test file.

The available modules are listed in CHRLINE-PatchV2/CHRLINE/object.py.
## Getting Started.

```sh
git clone https://github.com/k4zum4-sk/CHRLINE-PatchV2.git
```
## SET UP

You can run the setup with the following command:
python3 setup.py install

First, please try from `CHRLINE-PatchV2/test/login_getToken_test.py`.
- Make sure to specify the correct directory path for CHRLINE-PatchV2.

**Setting Environment Variables FOR MAC & WSL**

1. Check your shell type by running:  
   ```sh
   echo $SHELL
   ```
- If using zsh, add the variable to .zshrc:
  ```sh
  echo 'export CHRLINE_PATCH_PATH="Specify the correct directory path for CHRLINE-PatchV2"' >> ~/.zshrc
  ```
- If using bash, add the variable to .bashrc:
  ```sh
  echo 'export CHRLINE_PATCH_PATH="Specify the correct directory path for CHRLINE-PatchV2"' >> ~/.bashrc
  ```
2. Apply the settings:
- For zsh:
```sh
 source ~/.zshrc
```
- For bash:
```sh
source ~/.bashrc
```

3. Verify the variable is set:
```sh
echo $CHRLINE_PATCH_PATH
```

**Setting Environment Variables FOR WINDOWS**
1. For Command Prompt (cmd):
```sh
set CHRLINE_PATCH_PATH="Specify the correct directory path for CHRLINE-PatchV2"
```
2. For PowerShell:
 - To set the variable permanently:
 ```sh
 [System.Environment]::SetEnvironmentVariable("CHRLINE_PATCH_PATH", "Specify the correct directory path for CHRLINE-PatchV2", [System.EnvironmentVariableTarget]::User)
```
 - To set it only for the current session:
  ```sh
  $env:CHRLINE_PATCH_PATH = "Specify the correct directory path for CHRLINE-PatchV2"
  ```

#### Requirement ####

- Python 3.7
  - ~~pycrypto~~
  - **pycryptodomex**
  - xxhash
  - httpx[http2]
  - gevent
  - thrift
  - rsa
  - python-axolotl-curve25519
  - image
  - requests
  - qrcode
  - cryptography
  - rich

```sh
pip install pycryptodomex xxhash httpx gevent thrift rsa python-axolotl-curve25519 image requests qrcode cryptography rich
```

# Disclaimer:
- This project is not an official LINE API, and its use is at your own risk.
- It may violate LINE's terms of service, so it is not recommended for production use.


=========================== k4zum4 =========================
