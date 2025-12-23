# 🎯 CHRLINE-PatchV2 - スタートガイド (1ページ版)

最速でLINEメッセージを送信するための1ページガイド

---

## ⚡ 3分でスタート

### ステップ1: インストール（1分）

```bash
git clone https://github.com/k4zum4-sk/CHRLINE-PatchV2.git
cd CHRLINE-PatchV2
pip install -r requirements.txt
python setup.py install
```

### ステップ2: ログイン（1分）

```bash
python simple_login.py
```

1を選択 → QRコードをLINEアプリでスキャン → トークンをコピー

### ステップ3: メッセージ送信（1分）

```bash
python simple_send_message.py
```

1を選択 → 友達IDをコピー → 2を選択 → IDとメッセージを入力 → 送信

---

## 📱 フローチャート

```
┌─────────────────────────────────────────────┐
│  CHRLINE-PatchV2をクローン                    │
│  git clone https://...                      │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  依存関係をインストール                        │
│  pip install -r requirements.txt            │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  CHRLINEをインストール                        │
│  python setup.py install                    │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  セットアップ確認（オプション）                  │
│  python check_setup.py                      │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  ログイン                                     │
│  python simple_login.py                     │
│  ┌─────────────┬──────────────┐             │
│  │ QRコード    │ メール/PW     │             │
│  └─────────────┴──────────────┘             │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  トークンを取得して保存                        │
│  export LINE_AUTH_TOKEN="..."               │
│  または .line_token ファイルに保存            │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  メッセージ送信                               │
│  python simple_send_message.py              │
│  ┌─────────────┬──────────────┐             │
│  │ 友達一覧    │ メッセージ送信  │             │
│  └─────────────┴──────────────┘             │
└─────────────────────────────────────────────┘
```

---

## 🎯 コマンドチートシート

| やりたいこと | コマンド |
|------------|---------|
| インストール確認 | `python check_setup.py` |
| ログイン | `python simple_login.py` |
| 友達一覧を見る | `python simple_send_message.py` → 1 |
| メッセージ送信 | `python simple_send_message.py` → 2 |
| 全機能を試す | `python complete_workflow.py` |
| サンプル確認 | `python sample_usage.py` |

---

## ❓ よくあるエラーと解決方法

### `No module named 'CHRLINE'`
```bash
cd /path/to/CHRLINE-PatchV2
python setup.py install
```

### `No module named 'Crypto'`
```bash
pip uninstall pycrypto
pip install pycryptodomex
```

### `認証トークンが見つかりません`
```bash
python simple_login.py  # 新しいトークンを取得
```

### その他のエラー
```bash
python check_setup.py  # 詳細な診断
```

---

## 📚 もっと詳しく知りたい場合

### 日本語
- **完全ガイド.md** - すべての情報がまとまっている
- **使い方ガイド.md** - 詳細な手順とFAQ

### English
- **QUICK_START_GUIDE.md** - Complete English guide

---

## 🔐 セキュリティ注意

⚠️ **トークンは絶対に公開しない**
- GitHubにコミットしない
- SNSに投稿しない
- 他人に教えない

---

## ⚖️ 法的注意

⚠️ **非公式API** - 学習・研究目的のみで使用してください

---

## 🆘 困ったら

1. `python check_setup.py` でセットアップを確認
2. **使い方ガイド.md** のトラブルシューティングを確認
3. GitHub Issuesで質問

---

## 🎉 これで完了！

基本的な流れ：
1. インストール
2. ログイン（トークン取得）
3. メッセージ送信

**Happy Coding! 🚀**
