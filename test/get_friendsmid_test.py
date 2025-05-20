#友達全員の詳細(uid)を取得するテストコード

import sys
import os

# 環境変数からパスを取得
chrline_path = os.getenv("CHRLINE_PATCH_PATH")

if chrline_path:
    sys.path.insert(0, chrline_path)
else:
    print("環境変数 CHRLINE_PATCH_PATH が設定されていません\nREADME.mdを確認してください")
#パスを取得してからimprot
from CHRLINE import *
from CHRLINE.hooks import HooksTracer

# トークンを環境変数から読み込む
#token = os.getenv("LINE_AUTH_TOKEN", "")
if not token:
    raise ValueError("環境変数 'LINE_AUTH_TOKEN' が設定されていません。")



cl = CHRLINE(token, device="DESKTOPWIN") #ログイン処理
print("ログイン成功")

friend_list = cl.getAllContactIds() #友達全員のuidを取得

print(friend_list) 
