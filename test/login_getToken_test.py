#ログインして認証トークンを取得するテストコード

import sys
import os
# 環境変数からパスを取得
chrline_path = os.getenv("CHRLINE_PATCH_PATH")

if chrline_path:
    sys.path.insert(0, chrline_path)
else:
    print("環境変数 CHRLINE_PATCH_PATH が設定されていません\nREADME.mdを確認してください")
    sys.exit(1)
    
#パスを取得してからimprot
from CHRLINE import *
from CHRLINE.hooks import HooksTracer

#device -> "DESKTOPWIN","DESKTOPMAC","IOSIPAD","CHROMEOS","WATCHOS"

def login_web(): #emailとpasswordを入力してPINコードを受け取る
    e = input('Email: ')
    p = input('Password: ')
    try:
        return CHRLINE(e, p, device="IOSIPAD",useThrift=True) 
    except Exception as err:
        print(f"ログイン失敗: {err}")
        return None

def login_qr(): #.imagesディレクトリにQRコードが保存されるのでデバイスで読み込む
    try:
        return CHRLINE(device="DESKTOPWIN",useThrift=True) 
    except Exception as err:
        print(f"ログイン失敗: {err}")
        return None

def login_phone(): #電話番号と国を指定してログイン 例:09012345678, JP
    try:
        return CHRLINE(phone="", region="", device="IOSIPAD",useThrift=True) #このログイン方法は推奨しません。
    except Exception as err:
        print(f"ログイン失敗: {err}")
        return None
cl = login_qr()
#cl = login_phone() # 電話番号ログインを試す場合はこちらをコメント解除
#cl = login_web() # Webログインを試す場合はこちらをコメント解除
print("ログイン成功")
token = cl.authToken
print(f"authToken: {token}")
