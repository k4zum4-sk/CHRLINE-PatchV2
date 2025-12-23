#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完全なワークフロー例 / Complete Workflow Example
ログインからメッセージ送信までの一連の流れ
Complete flow from login to message sending
"""

import sys
import os
import time

# CHRLINEをインポート / Import CHRLINE
try:
    from CHRLINE import CHRLINE
except ImportError:
    print("❌ Error: CHRLINE is not installed.")
    print("Please run: pip install .")
    sys.exit(1)

class LineChatClient:
    def __init__(self):
        self.cl = None
        self.token = None
    
    def login_with_qr(self):
        """QRコードでログイン / Login with QR code"""
        print("\n📱 QRコードログイン / QR Code Login")
        print("=" * 60)
        print("QRコードを生成します。LINEアプリでスキャンしてください。")
        print("Generating QR code. Please scan with LINE app.")
        print()
        
        try:
            self.cl = CHRLINE(device="DESKTOPWIN", useThrift=True)
            self.token = self.cl.authToken
            print("✅ ログイン成功! / Login successful!")
            return True
        except Exception as e:
            print(f"❌ ログイン失敗 / Login failed: {e}")
            return False
    
    def login_with_email(self, email, password):
        """メールとパスワードでログイン / Login with email and password"""
        print("\n📧 メール&パスワードログイン / Email & Password Login")
        print("=" * 60)
        
        try:
            self.cl = CHRLINE(email, password, device="IOSIPAD", useThrift=True)
            self.token = self.cl.authToken
            print("✅ ログイン成功! / Login successful!")
            return True
        except Exception as e:
            print(f"❌ ログイン失敗 / Login failed: {e}")
            return False
    
    def login_with_token(self, token):
        """トークンでログイン / Login with token"""
        print("\n🔑 トークンでログイン / Token Login")
        print("=" * 60)
        
        try:
            self.cl = CHRLINE(token, device="DESKTOPWIN")
            self.token = token
            print("✅ ログイン成功! / Login successful!")
            return True
        except Exception as e:
            print(f"❌ ログイン失敗 / Login failed: {e}")
            return False
    
    def get_profile(self):
        """自分のプロフィールを取得 / Get own profile"""
        try:
            profile = self.cl.getProfile()
            print("\n👤 あなたのプロフィール / Your Profile:")
            print(f"   名前 / Name: {profile.displayName}")
            print(f"   MID: {profile.mid}")
            if hasattr(profile, 'statusMessage') and profile.statusMessage:
                print(f"   ステータス / Status: {profile.statusMessage}")
            return profile
        except Exception as e:
            print(f"❌ プロフィール取得失敗 / Failed to get profile: {e}")
            return None
    
    def get_friends(self):
        """友達一覧を取得 / Get friend list"""
        try:
            print("\n📋 友達一覧を取得中... / Getting friend list...")
            friend_ids = self.cl.getAllContactIds()
            
            friends = []
            for friend_id in friend_ids:
                try:
                    contact = self.cl.getContact(friend_id)
                    friends.append({
                        'id': friend_id,
                        'name': getattr(contact, 'displayName', 'Unknown'),
                        'status': getattr(contact, 'statusMessage', '')
                    })
                except:
                    friends.append({
                        'id': friend_id,
                        'name': 'Unknown',
                        'status': ''
                    })
            
            return friends
        except Exception as e:
            print(f"❌ 友達一覧取得失敗 / Failed to get friends: {e}")
            return []
    
    def display_friends(self, friends):
        """友達一覧を表示 / Display friend list"""
        print(f"\n✅ {len(friends)} 人の友達が見つかりました / friends found")
        print("\n友達の一覧 / Friend List:")
        print("=" * 60)
        
        for i, friend in enumerate(friends, 1):
            print(f"{i}. {friend['name']}")
            print(f"   ID: {friend['id']}")
            if friend['status']:
                print(f"   Status: {friend['status']}")
            print()
    
    def send_message(self, to_id, message):
        """メッセージを送信 / Send message"""
        try:
            print(f"\n📤 メッセージを送信中... / Sending message...")
            self.cl.sendMessage(to_id, message)
            print("✅ メッセージを送信しました! / Message sent successfully!")
            return True
        except Exception as e:
            print(f"❌ メッセージ送信失敗 / Failed to send message: {e}")
            return False

def main():
    print("=" * 60)
    print("CHRLINE-PatchV2 - Complete Workflow Example")
    print("完全なワークフロー例")
    print("=" * 60)
    print()
    
    client = LineChatClient()
    
    # ログイン方法を選択 / Select login method
    print("ログイン方法を選択してください / Select login method:")
    print("1. QRコードログイン (推奨) / QR Code Login (Recommended)")
    print("2. メール&パスワードログイン / Email & Password Login")
    print("3. トークンでログイン / Token Login")
    print()
    
    choice = input("選択 / Choice (1, 2, or 3): ").strip()
    
    # ログイン処理 / Login process
    login_success = False
    
    if choice == "1":
        login_success = client.login_with_qr()
    elif choice == "2":
        email = input("\nEmail: ").strip()
        password = input("Password: ").strip()
        login_success = client.login_with_email(email, password)
    elif choice == "3":
        token = input("\nToken: ").strip()
        login_success = client.login_with_token(token)
    else:
        print("❌ Invalid choice")
        sys.exit(1)
    
    if not login_success:
        print("\nログインに失敗しました / Login failed")
        sys.exit(1)
    
    # トークンを表示 / Display token
    if choice in ["1", "2"]:
        print(f"\n🔑 あなたの認証トークン / Your Auth Token:")
        print(f"   {client.token}")
        print("\n⚠️  このトークンを保存して、次回は「トークンでログイン」を使用できます")
        print("   Save this token to use \"Token Login\" next time")
    
    print("\n" + "=" * 60)
    time.sleep(1)
    
    # プロフィールを取得 / Get profile
    client.get_profile()
    time.sleep(1)
    
    # 友達一覧を取得 / Get friends
    friends = client.get_friends()
    if friends:
        client.display_friends(friends)
    
    print("\n" + "=" * 60)
    
    # メッセージ送信 / Send message
    print("\nメッセージを送信しますか？ / Do you want to send a message?")
    send = input("(y/n): ").strip().lower()
    
    if send == 'y':
        print("\n📨 メッセージ送信 / Send Message")
        print("=" * 60)
        
        to_id = input("送信先のID / Recipient ID: ").strip()
        message = input("メッセージ / Message: ").strip()
        
        if to_id and message:
            print(f"\n送信内容 / Sending:")
            print(f"  To: {to_id}")
            print(f"  Message: {message}")
            confirm = input("\n送信しますか？ / Send? (y/n): ").strip().lower()
            
            if confirm == 'y':
                client.send_message(to_id, message)
        else:
            print("❌ IDまたはメッセージが入力されていません / ID or message is required")
    
    print("\n" + "=" * 60)
    print("ワークフロー完了 / Workflow completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
