# CHRLINE 修正パッチ for JP
![logo](/examples/assets/logo.png)

まず、このライブラリの直接の開発者は私ではありません。
**DeachSword氏が全ての権利を保有**します

このプロジェクトは、Python非公式LINE APIであるCHRLINEの**循環インポート問題とインポートエラ**ーを修正したバージョンです。

CHRLINEを使うことで**個人アカウントのBOT化**などを実現できます

元のCHRLINEリポジトリ -> https://github.com/DeachSword/CHRLINE/tree/master

**具体的な修正内容**
**1. Windows環境での Crypto モジュールのエラー修正**
  - `from Crypto.Cipher import AES` などのインポートが Windows でエラーになる問題を修正
  - `CHRLINE-PatchV2/CHRLINE/e2ee.py,models.py` のインポート文 `Crypto` を `Cryptodome` に変更し、どの環境でも動作するよう統一
**2. 循環インポートとそれに関するエラーの修正**
 　- `thrift.py` というファイル名が公式の `thriftライブラリ`と衝突して循環インポートを起こしていたので`chrline_thrift.py`にリネーム
 　- `client.py`のインポート文を`chrline_thrift`に合わせて修正

- 日本語のコメント付きサンプルコードは `CHRLINE-PatchV2/test/` にあります。  

- 利用可能な API 一覧は `CHRLINE-PatchV2/CHRLINE/object.py` を参照してください。

## はじめに

まず、このリポジトリをクローンしてください：

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

まずは`CHRLINE-PatchV2/test/login_getToken_test.py`から試してみてください。

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
  set CHRLINE_PATCH_PATH "CHRLINE-PatchV2の正しいディレクトリパスを指定"
  ```
2. PowerShell の場合:
  ```sh
  [System.Environment]::SetEnvironmentVariable("CHRLINE_PATCH_PATH", "CHRLINE-PatchV2の正しいディレクトリパスを指定", [System.EnvironmentVariableTarget]::User)
  ```
  現在のセッションのみで有効 にする場合：
  ```sh
  $env:CHRLINE_PATCH_PATH = "CHRLINE-PatchV2の正しいディレクトリパスを指定"
  ```

#### 必要条件 ####

- Python 3.7
  - pycrypto
  - pycryptodome
  - xxhash
  - httpx[http2]
  - gevent

その他必要なモジュールは各々でインストールをお願いします

 - - - - - - # k4zum4 # - - - - - - 
# CHRLINE Patch for JP

First of all, I am not the direct developer of this library.
DeachSword holds all rights to it.

This project is a modified version of the unofficial LINE API, CHRLINE, that fixes circular import issues and import errors.

Specific changes:
 - The file thrift.py was conflicting with the thrift library, causing circular imports. It has been renamed to chrline_thrift.py to resolve the issue.
 - The import statements in client.py were modified to match the changes in chrline_thrift.

The basic usage in Japanese is described in the CHRLINE-PatchV2/test file.

The available modules are listed in CHRLINE-PatchV2/CHRLINE/object.py.
## First.

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
  - pycrypto
  - pycryptodome
  - xxhash
  - httpx[http2]
  - gevent

 - - - - - - # k4zum4 # - - - - - - 
