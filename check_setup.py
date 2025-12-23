#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
セットアップ確認スクリプト / Setup Verification Script
このスクリプトは、CHRLINE-PatchV2が正しくインストールされているか確認します。
This script verifies that CHRLINE-PatchV2 is correctly installed.
"""

import sys
import os

def check_python_version():
    """Pythonのバージョンを確認 / Check Python version"""
    print("=" * 60)
    print("Pythonバージョンの確認 / Checking Python Version")
    print("=" * 60)
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("❌ Python 3.6以上が必要です / Python 3.6+ is required")
        return False
    else:
        print("✅ Pythonバージョン: OK")
    return True

def check_module(module_name, import_path=None):
    """モジュールのインストールを確認 / Check module installation"""
    if import_path is None:
        import_path = module_name
    
    try:
        __import__(import_path)
        print(f"✅ {module_name}: インストール済み / Installed")
        return True
    except ImportError as e:
        print(f"❌ {module_name}: 未インストール / Not installed - {e}")
        return False

def check_dependencies():
    """依存関係を確認 / Check dependencies"""
    print("\n" + "=" * 60)
    print("依存関係の確認 / Checking Dependencies")
    print("=" * 60)
    
    modules = [
        ("pycryptodomex", "Cryptodome"),
        ("xxhash", "xxhash"),
        ("httpx", "httpx"),
        ("gevent", "gevent"),
        ("thrift", "thrift"),
        ("rsa", "rsa"),
        ("curve25519", "curve25519"),
        ("PIL", "PIL"),  # Pillow
        ("requests", "requests"),
        ("qrcode", "qrcode"),
        ("cryptography", "cryptography"),
        ("rich", "rich"),
    ]
    
    all_ok = True
    for display_name, import_name in modules:
        if not check_module(display_name, import_name):
            all_ok = False
    
    return all_ok

def check_chrline():
    """CHRLINEのインストールを確認 / Check CHRLINE installation"""
    print("\n" + "=" * 60)
    print("CHRLINEの確認 / Checking CHRLINE")
    print("=" * 60)
    
    try:
        from CHRLINE import CHRLINE
        print("✅ CHRLINE: インストール済み / Installed")
        
        # バージョン確認 / Check version
        try:
            from CHRLINE import __version__
            print(f"   Version: {__version__}")
        except:
            pass
        
        return True
    except ImportError as e:
        print(f"❌ CHRLINE: 未インストール / Not installed")
        print(f"   Error: {e}")
        print("\n修正方法 / How to fix:")
        print("   1. cd /path/to/CHRLINE-PatchV2")
        print("   2. python setup.py install")
        print("   または / or: pip install .")
        return False
    except Exception as e:
        print(f"❌ CHRLINE: エラー / Error")
        print(f"   Error: {e}")
        
        # 詳細なエラー情報 / Detailed error info
        import traceback
        print("\n詳細なエラー / Detailed error:")
        traceback.print_exc()
        return False

def check_environment():
    """環境変数を確認 / Check environment variables"""
    print("\n" + "=" * 60)
    print("環境変数の確認 / Checking Environment Variables")
    print("=" * 60)
    
    token = os.getenv("LINE_AUTH_TOKEN")
    if token:
        print("✅ LINE_AUTH_TOKEN: 設定済み / Set")
        print(f"   Token: {token[:20]}...")
    else:
        print("⚠️  LINE_AUTH_TOKEN: 未設定 / Not set")
        print("   これはオプションです / This is optional")
        print("   トークンを取得するには / To get a token:")
        print("   python simple_login.py")

def print_installation_guide():
    """インストールガイドを表示 / Show installation guide"""
    print("\n" + "=" * 60)
    print("インストールガイド / Installation Guide")
    print("=" * 60)
    print("\n1. 依存関係のインストール / Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n2. CHRLINEのインストール / Install CHRLINE:")
    print("   python setup.py install")
    print("   または / or: pip install .")
    print("\n3. ログイン / Login:")
    print("   python simple_login.py")
    print("\n4. メッセージ送信 / Send message:")
    print("   python simple_send_message.py")
    print("\n詳細なガイド / Detailed guide:")
    print("   日本語 / Japanese: 使い方ガイド.md")
    print("   English: QUICK_START_GUIDE.md")

def main():
    print("\n" + "=" * 60)
    print("CHRLINE-PatchV2 セットアップ確認")
    print("CHRLINE-PatchV2 Setup Verification")
    print("=" * 60)
    print()
    
    # Pythonバージョン確認 / Check Python version
    python_ok = check_python_version()
    
    # 依存関係確認 / Check dependencies
    deps_ok = check_dependencies()
    
    # CHRLINE確認 / Check CHRLINE
    chrline_ok = check_chrline()
    
    # 環境変数確認 / Check environment
    check_environment()
    
    # 結果サマリ / Result summary
    print("\n" + "=" * 60)
    print("確認結果 / Verification Result")
    print("=" * 60)
    
    if python_ok and deps_ok and chrline_ok:
        print("✅ すべての確認が完了しました！")
        print("✅ All checks passed!")
        print("\n次のステップ / Next steps:")
        print("   python simple_login.py")
    else:
        print("❌ いくつかの問題が見つかりました")
        print("❌ Some issues were found")
        print_installation_guide()
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
