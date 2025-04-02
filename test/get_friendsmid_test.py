#友達全員の詳細(mid)を取得するテストコード

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

# トークンを設定（手動入力 or 環境変数から取得）
token = "LINE_AUTH_TOKEN"  #login_getToken_test.pyで取得したトークンを入力 

# トークンをファイルや環境変数から読み込む方法も良い
#token = os.getenv("LINE_AUTH_TOKEN", "")


cl = CHRLINE(token, device="DESKTOPWIN") #ログイン処理
print("ログイン成功")

friend_list = cl.getAllContactIds() #友達全員の詳細を取得

print(friend_list) 
