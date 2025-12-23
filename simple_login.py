#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
簡単なログインスクリプト / Simple Login Script
QRコードでログインして認証トークンを取得します
Login with QR code and get authentication token
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

def main():
    print("=" * 60)
    print("CHRLINE-PatchV2 - Simple Login Script")
    print("=" * 60)
    print()
    
    print("ログイン方法を選択してください / Select login method:")
    print("1. QRコードログイン (推奨) / QR Code Login (Recommended)")
    print("2. メール&パスワードログイン / Email & Password Login")
    print()
    
    choice = input("選択 / Choice (1 or 2): ").strip()
    
    try:
        if choice == "1":
            # QRコードログイン / QR code login
            print("\n📱 QRコードを生成中... / Generating QR code...")
            print("   生成されたQRコードをLINEアプリでスキャンしてください")
            print("   Please scan the generated QR code with LINE app")
            print()
            
            cl = CHRLINE(device="DESKTOPWIN", useThrift=True)
            
        elif choice == "2":
            # メール&パスワードログイン / Email & password login
            print("\n📧 メールアドレスとパスワードを入力してください")
            print("   Enter your email and password")
            print()
            
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            
            if not email or not password:
                print("❌ Error: Email and password are required")
                sys.exit(1)
            
            print("\nログイン中... / Logging in...")
            cl = CHRLINE(email, password, device="IOSIPAD", useThrift=True)
            
        else:
            print("❌ Invalid choice")
            sys.exit(1)
        
        # ログイン成功 / Login successful
        print("\n" + "=" * 60)
        print("✅ ログイン成功! / Login Successful!")
        print("=" * 60)
        print()
        
        # トークンを取得 / Get token
        token = cl.authToken
        print(f"🔑 認証トークン / Auth Token:")
        print(f"   {token}")
        print()
        
        # 環境変数設定の案内 / Instructions for setting environment variable
        print("=" * 60)
        print("📝 次のステップ / Next Steps:")
        print("=" * 60)
        print()
        print("このトークンを環境変数に保存してください:")
        print("Save this token as an environment variable:")
        print()
        print("Linux/Mac:")
        print(f'  export LINE_AUTH_TOKEN="{token}"')
        print()
        print("Windows PowerShell:")
        print(f'  $env:LINE_AUTH_TOKEN = "{token}"')
        print()
        print("Windows CMD:")
        print(f'  set LINE_AUTH_TOKEN={token}')
        print()
        print("=" * 60)
        print("⚠️  注意 / Warning:")
        print("このトークンは誰にも共有しないでください!")
        print("Never share this token with anyone!")
        print("=" * 60)
        
        # トークンをファイルに保存（オプション）/ Save token to file (optional)
        print()
        save = input("トークンをファイルに保存しますか？ / Save token to file? (y/n): ").strip().lower()
        if save == 'y':
            with open('.line_token', 'w') as f:
                f.write(token)
            print("✅ トークンを '.line_token' に保存しました")
            print("   Token saved to '.line_token'")
            print("⚠️  このファイルを .gitignore に追加してください")
            print("   Add this file to .gitignore")
            
    except Exception as e:
        print("\n❌ エラーが発生しました / Error occurred:")
        print(f"   {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
