#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
簡単なメッセージ送信スクリプト / Simple Message Sending Script
友達にメッセージを送信します / Send messages to friends
"""

import sys
import os

# CHRLINEをインポート / Import CHRLINE
try:
    from CHRLINE import CHRLINE
except ImportError:
    print("❌ Error: CHRLINE is not installed.")
    print("Please run: pip install .")
    sys.exit(1)

def get_token():
    """トークンを取得 / Get token"""
    # 環境変数から取得 / Get from environment variable
    token = os.getenv("LINE_AUTH_TOKEN")
    
    if token:
        return token
    
    # .line_tokenファイルから取得 / Get from .line_token file
    if os.path.exists('.line_token'):
        with open('.line_token', 'r') as f:
            token = f.read().strip()
            if token:
                return token
    
    # トークンが見つからない / Token not found
    print("❌ Error: 認証トークンが見つかりません / Authentication token not found")
    print()
    print("トークンを設定してください / Please set your token:")
    print("1. 環境変数に設定 / Set as environment variable:")
    print('   export LINE_AUTH_TOKEN="your_token"')
    print()
    print("2. または .line_token ファイルを作成 / Or create .line_token file")
    print()
    print("トークンの取得方法 / How to get token:")
    print("   python simple_login.py")
    print()
    sys.exit(1)

def main():
    print("=" * 60)
    print("CHRLINE-PatchV2 - Simple Message Sending Script")
    print("=" * 60)
    print()
    
    # トークンを取得 / Get token
    token = get_token()
    
    # ログイン / Login
    try:
        print("🔐 ログイン中... / Logging in...")
        cl = CHRLINE(token, device="DESKTOPWIN")
        print("✅ ログイン成功! / Login successful!")
        print()
    except Exception as e:
        print(f"❌ ログイン失敗 / Login failed: {e}")
        print()
        print("トークンが無効または期限切れの可能性があります")
        print("Token may be invalid or expired")
        print("新しいトークンを取得してください: python simple_login.py")
        print("Get a new token: python simple_login.py")
        sys.exit(1)
    
    # 操作を選択 / Select operation
    print("操作を選択してください / Select operation:")
    print("1. 友達一覧を表示 / Show friend list")
    print("2. メッセージを送信 / Send message")
    print()
    
    choice = input("選択 / Choice (1 or 2): ").strip()
    
    try:
        if choice == "1":
            # 友達一覧を取得 / Get friend list
            print("\n📋 友達一覧を取得中... / Getting friend list...")
            friend_ids = cl.getAllContactIds()
            
            if not friend_ids:
                print("友達が見つかりませんでした / No friends found")
                return
            
            print(f"\n✅ {len(friend_ids)} 人の友達が見つかりました / friends found")
            print()
            
            # 各友達の詳細情報を取得 / Get details for each friend
            print("友達の詳細 / Friend details:")
            print("-" * 60)
            for i, friend_id in enumerate(friend_ids, 1):
                try:
                    contact = cl.getContact(friend_id)
                    display_name = getattr(contact, 'displayName', 'Unknown')
                    status_message = getattr(contact, 'statusMessage', '')
                    
                    print(f"{i}. {display_name}")
                    print(f"   ID: {friend_id}")
                    if status_message:
                        print(f"   Status: {status_message}")
                    print()
                except:
                    print(f"{i}. ID: {friend_id}")
                    print()
            
            print("-" * 60)
            print("💡 メッセージを送信するには、このIDをコピーして使用してください")
            print("   To send a message, copy and use one of these IDs")
            
        elif choice == "2":
            # メッセージを送信 / Send message
            print("\n📨 メッセージ送信 / Send Message")
            print("-" * 60)
            print()
            
            # 送信先IDを入力 / Enter recipient ID
            to_id = input("送信先のID / Recipient ID: ").strip()
            if not to_id:
                print("❌ Error: IDが入力されていません / ID is required")
                return
            
            # メッセージを入力 / Enter message
            message = input("メッセージ / Message: ").strip()
            if not message:
                print("❌ Error: メッセージが入力されていません / Message is required")
                return
            
            # 確認 / Confirmation
            print()
            print("送信内容を確認してください / Confirm sending:")
            print(f"  宛先 / To: {to_id}")
            print(f"  メッセージ / Message: {message}")
            print()
            
            confirm = input("送信しますか？ / Send? (y/n): ").strip().lower()
            if confirm != 'y':
                print("キャンセルしました / Cancelled")
                return
            
            # メッセージを送信 / Send message
            print("\n📤 送信中... / Sending...")
            cl.sendMessage(to_id, message)
            print("✅ メッセージを送信しました! / Message sent successfully!")
            
        else:
            print("❌ Invalid choice")
            return
            
    except Exception as e:
        print(f"\n❌ エラーが発生しました / Error occurred:")
        print(f"   {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
