#指定したmidに対してメッセージを送信するテストコード

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

to_Id = "" #例:get_friendsmid_test.pyなどで取得したmidを入力

cl = CHRLINE(token, device="DESKTOPWIN")#ログイン処理
print("ログイン成功")

cl.sendMessage(to_Id, "こんにちは！元気？")#送信処理