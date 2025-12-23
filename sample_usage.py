#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CHRLINE-PatchV2 サンプルコード
Sample Code for CHRLINE-PatchV2

このファイルは、CHRLINEの基本的な使い方を示すサンプルコードです。
This file demonstrates the basic usage of CHRLINE.

使い方 / Usage:
1. トークンを取得: python simple_login.py
2. このファイルを編集: YOUR_TOKEN と YOUR_FRIEND_ID を設定
3. 実行: python sample_usage.py
"""

from CHRLINE import CHRLINE

# =============================================================================
# 設定 / Configuration
# =============================================================================

# ここにあなたのトークンを入力してください
# Enter your token here
YOUR_TOKEN = "YOUR_AUTH_TOKEN_HERE"

# メッセージを送信したい相手のIDを入力してください
# Enter the recipient's ID
YOUR_FRIEND_ID = "u1234567890abcdef1234567890abcdef"

# 送信するメッセージ
# Message to send
YOUR_MESSAGE = "こんにちは！CHRLINEからのテストメッセージです。"

# =============================================================================
# メイン処理 / Main Process
# =============================================================================

def example_basic_usage():
    """基本的な使い方の例 / Basic usage example"""
    
    print("=" * 60)
    print("CHRLINE-PatchV2 サンプルコード")
    print("Sample Code for CHRLINE-PatchV2")
    print("=" * 60)
    print()
    
    # トークンのチェック / Check token
    if YOUR_TOKEN == "YOUR_AUTH_TOKEN_HERE":
        print("❌ エラー: トークンが設定されていません")
        print("❌ Error: Token is not set")
        print()
        print("手順 / Steps:")
        print("1. python simple_login.py を実行してトークンを取得")
        print("   Run python simple_login.py to get your token")
        print()
        print("2. このファイルを編集してYOUR_TOKENにトークンを設定")
        print("   Edit this file and set YOUR_TOKEN with your token")
        print()
        return
    
    try:
        # ステップ1: ログイン / Step 1: Login
        print("📝 ステップ1: ログイン / Step 1: Login")
        print("-" * 60)
        cl = CHRLINE(YOUR_TOKEN, device="DESKTOPWIN")
        print("✅ ログイン成功！ / Login successful!")
        print()
        
        # ステップ2: プロフィールを取得 / Step 2: Get profile
        print("📝 ステップ2: プロフィールを取得 / Step 2: Get profile")
        print("-" * 60)
        profile = cl.getProfile()
        print(f"名前 / Name: {profile.displayName}")
        print(f"MID: {profile.mid}")
        print()
        
        # ステップ3: 友達一覧を取得 / Step 3: Get friends
        print("📝 ステップ3: 友達一覧を取得 / Step 3: Get friends")
        print("-" * 60)
        friend_ids = cl.getAllContactIds()
        print(f"友達の数 / Number of friends: {len(friend_ids)}")
        
        # 最初の5人を表示 / Show first 5 friends
        print("\n最初の5人 / First 5 friends:")
        for i, friend_id in enumerate(friend_ids[:5], 1):
            try:
                contact = cl.getContact(friend_id)
                print(f"{i}. {contact.displayName} (ID: {friend_id})")
            except:
                print(f"{i}. ID: {friend_id}")
        print()
        
        # ステップ4: メッセージを送信 / Step 4: Send message
        if YOUR_FRIEND_ID != "u1234567890abcdef1234567890abcdef":
            print("📝 ステップ4: メッセージを送信 / Step 4: Send message")
            print("-" * 60)
            print(f"送信先 / To: {YOUR_FRIEND_ID}")
            print(f"メッセージ / Message: {YOUR_MESSAGE}")
            print()
            
            # 確認 / Confirmation
            confirm = input("送信しますか？ / Send? (y/n): ").strip().lower()
            if confirm == 'y':
                cl.sendMessage(YOUR_FRIEND_ID, YOUR_MESSAGE)
                print("✅ メッセージを送信しました！ / Message sent!")
            else:
                print("❌ キャンセルしました / Cancelled")
        else:
            print("📝 ステップ4: メッセージを送信 / Step 4: Send message")
            print("-" * 60)
            print("⚠️  YOUR_FRIEND_IDを設定してください")
            print("   Please set YOUR_FRIEND_ID")
        
        print()
        print("=" * 60)
        print("完了！ / Completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました / Error occurred:")
        print(f"   {str(e)}")
        print()
        print("トラブルシューティング / Troubleshooting:")
        print("- トークンが有効か確認してください")
        print("  Check if your token is valid")
        print("- インターネット接続を確認してください")
        print("  Check your internet connection")


def example_get_group_info():
    """グループ情報を取得する例 / Example: Get group info"""
    
    if YOUR_TOKEN == "YOUR_AUTH_TOKEN_HERE":
        print("トークンを設定してください / Please set your token")
        return
    
    try:
        cl = CHRLINE(YOUR_TOKEN, device="DESKTOPWIN")
        
        print("\n" + "=" * 60)
        print("グループ一覧 / Group List")
        print("=" * 60)
        
        # グループIDを取得 / Get group IDs
        group_ids = cl.getGroupIdsJoined()
        print(f"\n参加中のグループ数 / Number of joined groups: {len(group_ids)}")
        
        # 各グループの情報を表示 / Display group info
        for i, group_id in enumerate(group_ids, 1):
            try:
                group = cl.getGroup(group_id)
                print(f"\n{i}. {group.name}")
                print(f"   ID: {group_id}")
                print(f"   メンバー数 / Members: {len(group.members)}")
            except:
                print(f"\n{i}. ID: {group_id}")
        
    except Exception as e:
        print(f"エラー / Error: {e}")


def example_send_image():
    """画像を送信する例 / Example: Send image"""
    
    if YOUR_TOKEN == "YOUR_AUTH_TOKEN_HERE":
        print("トークンを設定してください / Please set your token")
        return
    
    if YOUR_FRIEND_ID == "u1234567890abcdef1234567890abcdef":
        print("YOUR_FRIEND_IDを設定してください / Please set YOUR_FRIEND_ID")
        return
    
    try:
        cl = CHRLINE(YOUR_TOKEN, device="DESKTOPWIN")
        
        # 画像ファイルのパス / Image file path
        image_path = input("画像ファイルのパス / Image file path: ").strip()
        
        if not image_path:
            print("画像パスが入力されていません / Image path not provided")
            return
        
        print(f"\n画像を送信中... / Sending image...")
        cl.sendImage(YOUR_FRIEND_ID, image_path)
        print("✅ 画像を送信しました！ / Image sent!")
        
    except Exception as e:
        print(f"エラー / Error: {e}")


# =============================================================================
# 実行 / Execution
# =============================================================================

if __name__ == "__main__":
    print("\n実行する例を選択してください / Select example to run:")
    print("1. 基本的な使い方 / Basic usage")
    print("2. グループ情報を取得 / Get group info")
    print("3. 画像を送信 / Send image")
    print()
    
    choice = input("選択 / Choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        example_basic_usage()
    elif choice == "2":
        example_get_group_info()
    elif choice == "3":
        example_send_image()
    else:
        print("無効な選択 / Invalid choice")
