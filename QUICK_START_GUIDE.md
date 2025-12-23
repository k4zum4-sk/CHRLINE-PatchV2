# CHRLINE-PatchV2 クイックスタートガイド / Quick Start Guide

このガイドでは、CHRLINE-PatchV2を使ってLINEメッセージを送信するまでの手順を説明します。
This guide explains how to set up CHRLINE-PatchV2 and send LINE messages.

---

## 📋 目次 / Table of Contents

1. [必要な環境 / Requirements](#必要な環境--requirements)
2. [インストール / Installation](#インストール--installation)
3. [ログインとトークン取得 / Login and Token Acquisition](#ログインとトークン取得--login-and-token-acquisition)
4. [メッセージ送信 / Sending Messages](#メッセージ送信--sending-messages)
5. [トラブルシューティング / Troubleshooting](#トラブルシューティング--troubleshooting)

---

## 必要な環境 / Requirements

- Python 3.6以上 / Python 3.6 or higher
- pip (Pythonパッケージマネージャー / Python package manager)

---

## インストール / Installation

### ステップ1: リポジトリのクローン / Step 1: Clone the Repository

```bash
git clone https://github.com/k4zum4-sk/CHRLINE-PatchV2.git
cd CHRLINE-PatchV2
```

### ステップ2: 依存関係のインストール / Step 2: Install Dependencies

```bash
pip install pycryptodomex xxhash httpx[http2] gevent thrift rsa python-axolotl-curve25519 pillow requests qrcode cryptography rich
```

**注意 / Note:** `Image`パッケージの代わりに`pillow`をインストールしてください。

### ステップ3: CHRLINEのインストール / Step 3: Install CHRLINE

```bash
python setup.py install
```

または / or:

```bash
pip install .
```

---

## ログインとトークン取得 / Login and Token Acquisition

### 方法1: QRコードログイン（推奨） / Method 1: QR Code Login (Recommended)

最も簡単で安全な方法です / This is the easiest and safest method.

1. `simple_login.py`を実行してください:
   Run `simple_login.py`:

```bash
python simple_login.py
```

2. 生成されたQRコードを**LINEアプリ**でスキャンしてください:
   - LINEアプリを開く / Open LINE app
   - 設定 → 他のデバイスでログイン → QRコードをスキャン
   - Settings → Login on another device → Scan QR code

3. 認証トークンが表示されます。これを保存してください。
   The authentication token will be displayed. Save it.

### 方法2: メールアドレスとパスワードログイン / Method 2: Email and Password Login

```python
from CHRLINE import CHRLINE

email = "your.email@example.com"
password = "your_password"

cl = CHRLINE(email, password, device="IOSIPAD", useThrift=True)
token = cl.authToken
print(f"Your token: {token}")
```

### トークンの保存 / Saving Your Token

取得したトークンは**環境変数**として保存することを推奨します:
It is recommended to save the token as an **environment variable**:

**Linux/Mac:**
```bash
export LINE_AUTH_TOKEN="your_token_here"
```

**Windows (PowerShell):**
```powershell
$env:LINE_AUTH_TOKEN = "your_token_here"
```

---

## メッセージ送信 / Sending Messages

### ステップ1: 友達のIDを取得 / Step 1: Get Friend IDs

```python
from CHRLINE import CHRLINE
import os

token = os.getenv("LINE_AUTH_TOKEN")
cl = CHRLINE(token, device="DESKTOPWIN")

# 友達一覧を取得 / Get friend list
friend_ids = cl.getAllContactIds()
print("Friend IDs:", friend_ids)
```

### ステップ2: メッセージを送信 / Step 2: Send a Message

`simple_send_message.py`を使用してください:
Use `simple_send_message.py`:

```bash
python simple_send_message.py
```

または手動で / Or manually:

```python
from CHRLINE import CHRLINE
import os

token = os.getenv("LINE_AUTH_TOKEN")
cl = CHRLINE(token, device="DESKTOPWIN")

# 友達のIDを指定 / Specify friend ID
to_id = "u1234567890abcdef1234567890abcdef"

# メッセージを送信 / Send message
cl.sendMessage(to_id, "こんにちは！Hello!")
print("Message sent successfully!")
```

---

## トラブルシューティング / Troubleshooting

### エラー: `No module named 'Crypto'`

**解決方法 / Solution:**

```bash
pip uninstall pycrypto
pip install pycryptodomex
```

### エラー: `Circular import error`

このパッチバージョンでは修正済みです。もし発生する場合は:
This has been fixed in this patched version. If it still occurs:

1. `thrift.py`が`chrline_thrift.py`にリネームされていることを確認
   Verify that `thrift.py` has been renamed to `chrline_thrift.py`

2. 再インストール / Reinstall:
   ```bash
   pip uninstall CHRLINE
   python setup.py install
   ```

### エラー: 認証失敗 / Authentication Failed

1. トークンが正しいか確認 / Verify token is correct
2. トークンの有効期限が切れていないか確認 / Check if token has expired
3. 新しいトークンを取得 / Get a new token

### エラー: `LINE_AUTH_TOKEN が設定されていません`

環境変数が設定されていません。上記の「トークンの保存」セクションを参照してください。
The environment variable is not set. Refer to the "Saving Your Token" section above.

---

## 🔐 セキュリティに関する注意 / Security Notes

- トークンは**絶対に**公開しないでください / **Never** share your token publicly
- トークンをソースコードに直接記述しないでください / Don't hardcode tokens in source code
- 環境変数を使用してください / Use environment variables
- `.gitignore`にトークンファイルを追加してください / Add token files to `.gitignore`

---

## ⚠️ 免責事項 / Disclaimer

- これは**非公式のLINE API**です / This is an **unofficial LINE API**
- 使用は自己責任でお願いします / Use at your own risk
- LINEの規約に違反する可能性があります / May violate LINE's terms of service
- **学習・研究目的のみ**での使用を推奨 / Recommended for **educational and research purposes only**

---

## 📚 さらに詳しく / Learn More

- サンプルコード: `test/` ディレクトリ / Sample code: `test/` directory
- 高度な使用例: `examples/` ディレクトリ / Advanced examples: `examples/` directory
- グループBOT: `test/group_bot.py` / Group bot: `test/group_bot.py`
- オープンチャットBOT: `test/square_bot.py` / Open chat bot: `test/square_bot.py`

---

## 🆘 サポート / Support

問題が発生した場合は、GitHubのIssuesで報告してください:
If you encounter issues, please report on GitHub Issues:

https://github.com/k4zum4-sk/CHRLINE-PatchV2/issues

---

**Happy Coding! 🚀**
